"""
database.py - 参数化数据库访问层（供 logs_store.py / fetch_changelog.py 使用）

与 common.py 里的 db_job_latest 并存：那份是历史实现（f-string 拼 SQL、每题一句新连接），
继续留给既有爬虫脚本用；新写的更新日志落库统一走本模块，原因有三：

1. 全部用 %s 占位符参数化——日志文本里带单引号、百分号、反斜杠的概率很高，
   拼接式 SQL 会被直接拼坏（hub 那边还专门把 % 替换成 $$ 绕开）；
2. 共享一条 autocommit 连接——批量补日志时每个 ROM 都要读写 logs 表，
   反复建连既慢又容易在长跑任务里断连；
3. execute(..., raise_on_error=True) 让写失败显形——默认行为（吞异常返回 None）
   会让「写失败」和「查不到」无法区分，日志补写会静默丢数据。
"""
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from pymysql import Connection

import config

logger = logging.getLogger(__name__)


class DatabaseManager:
	"""数据库操作管理（参数化 + 连接复用）"""

	_shared: Optional[Connection] = None

	# ==================== 连接 ====================

	@classmethod
	def _connection(cls) -> Connection:
		"""获取共享连接（断了自动重连）"""
		if cls._shared is not None:
			try:
				cls._shared.ping(reconnect=True)
				return cls._shared
			except Exception:
				try:
					cls._shared.close()
				except Exception:
					pass
				cls._shared = None
		cls._shared = Connection(
			user=config.user,
			password=config.password,
			host=config.host,
			port=config.port,
			database=config.database,
			autocommit=True,
			connect_timeout=10,
			read_timeout=30,
			write_timeout=30,
		)
		return cls._shared

	@classmethod
	def close(cls) -> None:
		"""关闭共享连接（长驻进程退出前调用）"""
		if cls._shared is not None:
			try:
				cls._shared.close()
			except Exception:
				pass
			cls._shared = None

	# ==================== 执行 ====================

	@classmethod
	def execute(
		cls,
		sql: str,
		params: Optional[Union[Tuple, List, Dict]] = None,
		fetch_one: bool = False,
		raise_on_error: bool = False,
	) -> Union[Tuple, List[Tuple], None]:
		"""执行参数化 SQL

		Args:
			sql: 使用 %s 作占位符的 SQL（无占位符时直接传原生 SQL）
			params: 占位符参数（元组/列表/字典）；为 None 时不做参数插值
			fetch_one: 只取首条记录
			raise_on_error: 出错时是否抛出。默认 False 保持历史行为（记日志后返回 None），
				写入类调用请传 True，避免写失败被当成空结果静默吞掉。

		Returns:
			单条记录（元组）或全部记录（列表）；出错且 raise_on_error=False 时返回 None
		"""
		cursor = None
		try:
			cursor = cls._connection().cursor()
			# 没有参数时不能给 execute 传空元组，否则 SQL 里的字面量 % 会被当成占位符
			if params is None:
				cursor.execute(sql)
			else:
				cursor.execute(sql, params)
			return cursor.fetchone() if fetch_one else cursor.fetchall()
		except Exception as exc:
			logger.error(f"SQL执行错误: {sql[:120]}..., 错误: {type(exc).__name__}: {exc}")
			if raise_on_error:
				raise
			return None
		finally:
			if cursor is not None:
				cursor.close()

	@classmethod
	def insert(
		cls,
		sql: str,
		params: Optional[Union[Tuple, List, Dict]] = None,
		raise_on_error: bool = False,
	) -> int:
		"""执行 INSERT 并返回自增主键（lastrowid），失败返回 0"""
		cursor = None
		try:
			cursor = cls._connection().cursor()
			if params is None:
				cursor.execute(sql)
			else:
				cursor.execute(sql, params)
			return int(cursor.lastrowid or 0)
		except Exception as exc:
			logger.error(f"SQL插入错误: {sql[:120]}..., 错误: {type(exc).__name__}: {exc}")
			if raise_on_error:
				raise
			return 0
		finally:
			if cursor is not None:
				cursor.close()

	@classmethod
	def execute_many(
		cls,
		sql: str,
		seq_params: Sequence,
		raise_on_error: bool = False,
	) -> int:
		"""批量执行同一条参数化 SQL（executemany），返回受影响行数"""
		cursor = None
		try:
			cursor = cls._connection().cursor()
			cursor.executemany(sql, seq_params)
			return cursor.rowcount if cursor.rowcount and cursor.rowcount > 0 else 0
		except Exception as exc:
			logger.error(f"SQL批量执行错误: {sql[:120]}..., 错误: {type(exc).__name__}: {exc}")
			if raise_on_error:
				raise
			return 0
		finally:
			if cursor is not None:
				cursor.close()

	# ==================== 查询 ====================

	@classmethod
	def query_one(cls, sql: str, params: Optional[Union[Tuple, List, Dict]] = None) -> Optional[Tuple]:
		"""查询单条记录"""
		return cls.execute(sql, params=params, fetch_one=True)

	@classmethod
	def query_all(cls, sql: str, params: Optional[Union[Tuple, List, Dict]] = None) -> List[Tuple]:
		"""查询全部记录（无结果时返回空列表，不返回 None）"""
		result = cls.execute(sql, params=params, fetch_one=False)
		return result if result else []

	# ==================== 信息 ====================

	@classmethod
	def target(cls) -> str:
		"""返回实际连接的库，便于运行前确认「脚本写的是哪个库」"""
		return f"{config.user}@{config.host}:{config.port}/{config.database}"
