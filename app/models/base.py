# -*- coding: utf-8 -*-
"""
(C) Guangcai Ren <rgc@bvrft.com>
All rights reserved
"""
# # pylint: disable=no-member
import copy
import traceback

from flask import current_app
from sqlalchemy import and_, update, select, func, or_, desc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

from app.core import db, logger


class BaseModel(object):
    """mysql操作基类"""

    @classmethod
    def get_obj_by_field(cls, search: list):
        """
        通过删选条件获取符合条件的第一个数据对象

        :param search:删选条件
        :return:obj
        """
        return cls.query.filter(and_(*search)).first()

    @classmethod
    def get_obj_by_field_all(cls, search: list):
        """
        通过删选条件获取符合条件的所有数据对象

        :param search:删选条件
        :return:
        """
        return cls.query.filter(and_(*search)).all()

    @classmethod
    def create(cls, info=None, auto_commit=True, session=None, unique_catch=False):
        """

        :param info: 添加的数据,dict
        :param auto_commit:是否自动提交
        :param unique_catch:是否捕捉 提交数据库时的unique 错误
        :return:
        """
        if not info:
            info = dict
        order = cls(**info)
        if not session:
            session = db.session
        try:
            session.add(order)
            if auto_commit:
                session.commit()
        except SQLAlchemyError as e:
            logger.error(traceback.format_exc())
            if unique_catch and isinstance(e, IntegrityError):
                return 'not_unique'
            return 'db_error'
        return 'success'

    @classmethod
    def insert_many(cls, info_list, auto_commit=True):
        """
        批量插入数据
        用法优化:放在最后的数据操作 可以 使用 auto_commit=True 从而提交所有对数据库的操作,不用在业务层显示使用 Model.commit()
        警告点：如果出现集中commit()的情况时，在执行完此 语句后，要判断是否执行成功，因为在执行 session.execute就可能触发错误，
               并且在集中commit()时，此错误不会再次捕捉，从而造成批量插入失败，但是返回成功 的业务逻辑错误
        集中commit()的情况下,执行此语句时，避免错误的使用方法：
        >>> if not Model.insert_many(info_list, False):
        >>>     return json_fail(code_dict['db_error'])

        :param info_list: format:[{},{}]
        :param auto_commit:
        :return:
        """
        session = db.session
        try:
            # 因为如果info_list 为空数据，同样会插入数据库一条数据，所以要有限制
            if info_list:
                session.execute(cls.__table__.insert(), info_list)
                if auto_commit:
                    session.commit()
        except SQLAlchemyError:
            logger.error(traceback.format_exc())
            session.rollback()
            return False
        return True

    @classmethod
    def insert_many_update(cls, info_list, field, auto_commit=True):
        """
        批量插入更新数据，如果存在就更新，如果不存在就插入
        用法优化:放在最后的数据操作 可以 使用 auto_commit=True 从而提交所有对数据库的操作,不用在业务层显示使用 Model.commit()
        警告点：如果出现集中commit()的情况时，在执行完此 语句后，要判断是否执行成功，因为在执行 session.execute就可能触发错误，
               并且在集中commit()时，此错误不会再次捕捉，从而造成批量插入失败，但是返回成功 的业务逻辑错误
               第一次使用会 报警告 SAWarning: Can't validate argument 'append_string';
                                can't locate any SQLAlchemy dialect named 'append'
        集中commit()的情况下,执行此语句时，避免错误的使用方法：
        >>> if not Model.insert_many([{'key':1,'key2':2},{'key':1,'key2':2}], 'sec_id',False):
        >>>     return json_fail(code_dict['db_error'])

        :param info_list: format:[{},{}]
        :param field: 需要修改的字段
        :param auto_commit:
        :return:
        """

        @compiles(Insert)
        def append_string(insert, compiler, **kw):  # pylint: disable=unused-variable
            s = compiler.visit_insert(insert, **kw)
            if 'append_string' in insert.kwargs:
                return s + " " + insert.kwargs['append_string']
            return s

        session = db.session
        try:
            # 因为如果info_list 为空数据，同样会插入数据库一条数据，所以要有限制
            if info_list:
                session.execute(
                    cls.__table__.insert(append_string='on DUPLICATE KEY UPDATE `{0}` = VALUES(`{0}`)'.format(field)),
                    info_list)
                if auto_commit:
                    session.commit()
        except SQLAlchemyError:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            session.rollback()
            return False
        return True

    def to_dict(self, keys: list):
        """
        把查询结果的对象转为dict

        :param keys:需要转换的字段
        :return:
        """
        d = {}
        for k in keys:
            d[k] = getattr(self, k)
        return d

    @classmethod
    def get_model_columns(cls, names=None):
        """
        获取 Model 的类型为 Column 的属性
        主要用于 db.session.query(columns)
        减少数据量
        """
        if not names:
            return []
        return [getattr(cls, name) for name in names]

    @classmethod
    def info(cls, search, field):
        """
        查询一条数据的全部字段(不利于IO,尽量只查需要的字段)，再取部分值
        :param search_list: 搜索列表
        :param field_list: 返回字段列表
        :return:
        """
        ins = cls.query.filter(and_(*search)).first()
        if ins is None:
            return dict()
        return ins.to_dict(keys=field)

    @classmethod
    def info_all(cls, search_list, field_list):
        """
        查询所有数据的全部字段(不利于IO,尽量只查需要的字段)，再取部分值
        :param search_list: 搜索列表
        :param field_list: 返回字段列表
        :return:
        """
        ins = cls.query.filter(and_(*search_list)).all()
        if ins is None:
            return None
        return list(
            map(
                lambda x: x.to_dict(field_list), ins
            )
        )

    @classmethod
    def info_all_or(cls, search_list):
        """
        查询所有数据的全部字段(不利于IO,尽量只查需要的字段)，再取部分值
        :param search_list: 搜索列表
        :param field_list: 返回字段列表
        :return:
        """
        return cls.query.filter(or_(*search_list)).all()

    @classmethod
    def info_all_and_query(cls, search, *field):
        """

        :param search: list,里面可以进行in,== 查询 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 传变量 如: AttMacroState.type
        :return:list ((0,),)

        usage:
        >>> Model.info_all_and_query([Model.sec_id == sec_id,
        >>>                           Model.user_id.in_(list(add_set))], Model.user_id
        """
        return db.session.query(*field).filter(and_(*search)).all()

    @classmethod
    def info_all_or_query(cls, search, *field):
        """

        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(or_(*search)).all()

    @classmethod
    def info_first_and_query(cls, search, *field):
        """

        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(and_(*search)).first()

    @classmethod
    def query_limit2(cls, search, orderby, *field):
        """
        查询最后的两个数据
        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(and_(*search)).order_by(orderby).limit(2).all()

    @classmethod
    def info_scalar_and_query(cls, search, *field):
        """
        查询第一条符合条件的数据，scalar的用法为 如果 first()的结果为 ['df'] ;则 scalar 为 'df';比first多了一步从list中取数据的功能
        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(and_(*search)).scalar()

    @classmethod
    def info_scalar_or_query(cls, search, *field):
        """
        查询第一条符合条件的数据，scalar的用法为 如果 first()的结果为 ['df'] ;则 scalar 为 'df';比first多了一步从list中取数据的功能
        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(or_(*search)).scalar()

    @classmethod
    def info_first_and_query_order(cls, search, order_field, *field):
        """

        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param order_field: 传需要排序的变量 如: AttMacroState.id
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(and_(*search)).order_by(order_field.desc()).first()

    @classmethod
    def get_first_data(cls, input):
        """
        对应 使用 .first() 查询一个字段的数据，要求 返回 字段值 或者 None
        :param input:
        :return:
        """
        if not input or not input[0]:
            return None
        return input[0]

    @classmethod
    def info_all_and_group_order(cls, search, group, order_field, *field):
        """

        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param order_field: 传需要排序的变量 如: AttMacroState.id
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(and_(*search)).group_by(group).order_by(order_field.desc()).all()

    @classmethod
    def info_all_and_query_order(cls, search, order_field, *field):
        """

        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param order_field: 传需要排序的变量 如: AttMacroState.id
        :param field: 传变量 如: AttMacroState.type
        :return:
        """
        return db.session.query(*field).filter(and_(*search)).order_by(order_field).all()

    @classmethod
    def info_first_or_query(cls, search, *field):
        """

        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 变量 如：AttMacroState.id
        :return:
        """
        return db.session.query(*field).filter(or_(*search)).first()

    @classmethod
    def update(cls, search: list, data: dict, auto_commit=True, session=False):
        """
        更新符合条件的多条数据

        :param search:搜素条件
        :param data:需要修改的数据
        :param auto_commit:是否自动提交
        :param session:
        :return:

        Usage:
        >>> update([model.type == 1, model.status == 1], {'val':1}, auto_commit=True)
        """
        if not session:
            session = db.session
        try:
            session.execute(
                update(cls).where(and_(*search)).values(**data)
            )
            if auto_commit:
                session.commit()
        except SQLAlchemyError:
            logger.error(traceback.format_exc())
            session.rollback()
            return False

        return True

    @classmethod
    def update_many_in(cls, in_field, search, del_set, data, auto_commit=True):
        """

        :param in_field:  Model.field
        :param search:  Model.field = val
        :param del_set: list or set [1,2,3]
        :param data: dict
        :param auto_commit: bool
        :return:bool

        usage:
        >>> Model.update_many_in(Model.user_id,Model.sec_id==1, [1,2,3], {'state': 1}, False)
        """

        db.session.execute(update(cls).where(and_(in_field.in_(del_set), search)).values(**data))
        if auto_commit:
            try:
                db.session.commit()
            except SQLAlchemyError:
                logger.error(traceback.format_exc())
                db.session.rollback()
                return False

        return True

    @classmethod
    def exist(cls, search):
        """

        :param search: dict 如：{"product_id": product_id, "status": 1}
        :return:
        """
        return db.session.query(cls.query.filter_by(**search).exists()).scalar()

    @classmethod
    def exist_by_obj(cls, search):
        """

        :param search:list 如：[Model.id == id, Model.state != state]
        :return: bool
        """
        return db.session.execute(
            select([func.count(cls.id)]).where(
                and_(*search)
            )
        ).fetchone()[0] >= 1

    @classmethod
    def map_dict(cls, sql):
        """
        sql查询结果转为map

        :param sql:
        :return:
        """
        return map(dict, db.session.execute(sql))

    @classmethod
    def list_map_dict(cls, sql):
        """
        sql查询结果转为list

        :param sql:
        :return:
        """
        return list(cls.map_dict(sql))

    @classmethod
    def get_sum(cls, sum_field, filter):
        """
        对字段求和

        :param sum_field:需要被求和的字段
        :param filter:删选条件
        :return:
        """
        c = db.session.execute(
            select([func.sum(sum_field)]).where(and_(*filter))
        ).fetchone()[0] or 0
        return c

    @classmethod
    def get_count(cls, count_field, filter):
        """获取表总条数

        Usage:
            >>>get_count(model.id,[model.name=='df'])

        :param count_field:
        :param filter:
        :return:
        """
        c = db.session.execute(
            select([func.count(count_field)]).where(and_(*filter))
        ).fetchone()[0] or 0
        return c

    @classmethod
    def get_max(cls, max_field, filter=None):
        """
        获取字段最大值

        :param max_field: 需要查询的字段
        :param filter: 删选条件
        :return:
        """
        stmt = select([func.max(max_field)])
        if filter:
            stmt = stmt.where(and_(*filter))
        c = db.session.execute(stmt).fetchone()[0]
        return c

    @classmethod
    def pagination(cls, page_index: int, page_size: int, field: list, search: list):
        """
        分页获取数据

        :param page_index: 数据页 从1 开始
        :param page_size: 每页大小
        :param field: 转为dict的字段列表
        :param search: 删选条件
        :return:
        """
        result = cls.query.filter(and_(*search)).paginate(int(page_index), int(page_size), False)
        result_list = []
        for item in result.items:
            result_list.append(item.to_dict(keys=field))
        return result_list

    @classmethod
    def pagination_order(cls, page_index: int, page_size: int, field: list, search: list, order):
        """
        分页获取数据

        :param page_index: 数据页 从1 开始
        :param page_size: 每页大小
        :param field: 转为dict的字段列表
        :param search: 删选条件
        :param order: 排序
        :return:
        """
        result = cls.query.filter(and_(*search)).order_by(order).paginate(int(page_index), int(page_size), False)
        result_list = []
        for item in result.items:
            result_list.append(item.to_dict(keys=field))
        return result_list

    @classmethod
    def commit(cls, session=None):
        """
        提交数据

        :param session:
        :return:
        """
        try:
            if not session:
                session = db.session
            session.commit()
        except Exception:
            logger.error(traceback.format_exc())
            session.rollback()
            return False
        return True

    @classmethod
    def flush(cls, session=None):
        """
        flush数据

        :param session:
        :return:
        """
        try:
            if not session:
                session = db.session
            session.flush()
        except Exception:
            session.rollback()
            return False
        return True

    @classmethod
    def get_comment(cls, fields=None):
        """
        获取orm的所有带 comment 的 字段属性
        :return:
        """
        return_dict = {}
        if not fields:
            fields = dir(cls)
        for item in fields:
            try:
                comment = getattr(cls, item).comment
                if comment:
                    return_dict[item] = comment
            except AttributeError:
                pass
        return return_dict

    @classmethod
    def get_comment_list(cls, fields=None):
        """
        获取 model 字段及其备注, 该方法返回的是列表
        顺序即传入的 fields 的顺序

        :return: 返回二元元组列表
        :rtype: [(field, comment)]
        """
        result = []
        if not fields:
            fields = dir(cls)
        for field in fields:
            comment = getattr(cls, field).comment
            result.append([field, comment])
        return result

    @classmethod
    def get_order_first(cls, search, *field):
        """
        获取排序的第一个值
        :param search: list 如:[AttMacroStateModel.type == 1, AttMacroStateModel.status == 1]
        :param field: 变量 如：AttMacroState.id
        :return:tuple
        """
        return db.session.query(*field).order_by(desc(search)).first()

    @classmethod
    def get_like_search(cls, like_field_tuple_list, other_dict, page_size, page_num, *query_field):
        """
        like模糊查询

        :param like_field_tuple_list: 模糊查询的字段及值 如 [(Model.id,1),(Model.name,2)]
        :param other_dict: 其他需要放入dict的字段及值
        :param page_size: 每页大小
        :param page_num: 当前页数
        :param query_field: 查询的字段 如 [Model.id,Model.name]
        :return:
        """
        if not other_dict:
            other_dict = {}
        query = db.session.query(*query_field)
        for item in like_field_tuple_list:
            if item[1]:
                query = query.filter(item[0].like("%{}%".format(item[1])))

        # 是否分页查询数据
        if page_size and page_num:
            result = query.limit(page_size).offset(
                (page_num - 1) * page_size)
        else:
            result = query.all()

        return_list = []
        for item in result:
            other_dict = copy.deepcopy(other_dict)
            count = 0
            for qu in query_field:
                other_dict.update({qu.key: item[count]})
                count += 1
            return_list.append(other_dict)
        return return_list

    @classmethod
    def get_like_count(cls, like_field_tuple_list, query_field):
        """
        like模糊查询总条数
        :param like_field_tuple_list:  模糊查询的字段及值 如 [(Model.id,1),(Model.name,2)]
        :param other_dict:  其他需要放入dict的字段及值
        :param query_field: 查询的字段 如 [Model.id,Model.name]
        :return:
        """

        query = db.session.query(func.count(query_field))
        for item in like_field_tuple_list:
            if item[1]:
                query = query.filter(item[0].like("%{}%".format(item[1])))

        result = query.all()
        return result[0][0]

    @classmethod
    def sql_execute(cls, str_sql, bind_key, query_one=True):
        """
        原始sql查询数据查询数据
        :param str_sql:
        :param bind_key:数据库名称
        :param query_one: 是否查询一条数据
        :return:
        """
        cursor = db.get_engine(current_app, bind_key)
        execute_obj = cursor.execute(str_sql)
        if query_one:
            return execute_obj.fetchone()
        return execute_obj.fetchall()

    @classmethod
    def del_all(cls, search=None, commit=False):
        """
        删除符合条件的所有数据
        :param model:
        :param search:
        :param commit:
        :return:
        """
        session = db.session
        try:
            if not search:
                session.query(cls).delete()
            else:
                session.query(cls).filter(and_(*search)).delete()

            if commit:
                session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False
