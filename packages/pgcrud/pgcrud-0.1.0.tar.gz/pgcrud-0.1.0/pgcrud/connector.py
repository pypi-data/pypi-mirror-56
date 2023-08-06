from psycopg2 import connect
from typing import List, Any, Iterator
import logging

log = logging.Logger(__name__)


class Connector:

    def __init__(self,
                 host: str,
                 dbname: str,
                 user: str,
                 password: str):
        self.creds = f"host={host} dbname={dbname} \
                      user={user} password={password}"
        self.conn = None

    def _get_conn(self) -> connect:
        return self.conn if self.conn else connect(self.creds)

    def commit(self):
        self.conn.commit()
        self.conn.close()
        self.conn = None

    def _execute(self,
                 sql: str,
                 values: List[Any]
                 ):
        log.debug(sql)
        log.debug(values)
        self.conn = self._get_conn()
        cur = self.conn.cursor()
        cur.execute(sql, values)
        return cur

    def _dict_to_cr(self, data: dict) -> (str, str, List[Any]):
        values = [v for __, v in data.items()]
        fld_lst = [k for k in data]
        fields = ','.join(fld_lst)
        var_lst = ['%s' for __ in range(len(data))]
        variables = ','.join(var_lst)
        return fields, variables, values

    def create(self,
               table: str,
               data: dict,
               commit: bool = True
               ) -> None:
        fields, variables, values = self._dict_to_cr(data)
        sql = f'INSERT INTO {table}({fields})VALUES({variables})'
        self._execute(sql, values)
        if commit:
            self.commit()

    def _find_val_pos(self, criteria: str, i: int) -> int:
        parts = criteria.split('%s', i+1)
        if len(parts) <= i + 1:
            return -1
        return len(criteria)-len(parts[-1])-2

    def _flatten_values(self, values: List[Any]) -> List[Any]:
        flat_values = []
        for val in values:
            if type(val) == list:
                flat_values.extend(val)
            else:
                flat_values.append(val)
        return flat_values

    def _replace_criteria(self, criteria: str, i: int, num_vals: int) -> str:
        loc = self._find_val_pos(criteria, i)
        cr_l = ['%s' for __ in range(num_vals)]
        cr_s = ','.join(cr_l)
        cr_ins = f'({cr_s})'
        b = criteria[:loc]
        a = criteria[loc+2:]
        return b + cr_ins + a

    def _in_criteria(self,
                     criteria: str = None,
                     values: List[Any] = None
                     ) -> (str, List[Any]):
        if values:
            if not criteria:
                raise Exception('Criteria are require to set criteria values')
            i = 0
            for value in values:
                if type(value) == list:
                    criteria = self._replace_criteria(criteria, i, len(value))
                    i += len(value)
                else:
                    i += 1
            return criteria, self._flatten_values(values)
        else:
            return criteria, None

    def _dict_to_up(self, data: dict) -> (str, List[Any]):
        updates = [f'{str(k)} = %s' for k in data]
        values = [v for __, v in data.items()]
        update = ','.join(updates)
        return update, values

    def update(self,
               table: str,
               data: dict,
               criteria: str = None,
               values: List[Any] = None
               ) -> None:
        crit, vals = self._in_criteria(criteria, values)
        update, up_vals = self._dict_to_up(data)
        full_vals = up_vals + vals if vals else up_vals
        sql_base = f'UPDATE {table} SET {update} '
        sql = sql_base + crit if crit else sql_base
        self._execute(sql, full_vals)
        self.commit()

    def delete(self,
               table: str,
               criteria: str = None,
               values: List[Any] = None,
               commit: bool = True
               ) -> None:
        crit, vals = self._in_criteria(criteria, values)
        sql_base = f'DELETE FROM {table} '
        sql = sql_base + crit if crit else sql_base
        self._execute(sql, vals)
        if commit:
            self.commit()

    def _row_to_dict(self, fields: List[str], row: List[list]) -> List[dict]:
        return {fields[i]: v for i, v in enumerate(row)}

    def list_select(self,
               table: str,
               fields: List[str],
               criteria: str = None,
               values: List[Any] = None,
               commit: bool = True
               ) -> List[dict]:
        crit, vals = self._in_criteria(criteria, values)
        flds = ','.join(fields)
        sql_base = f'SELECT {flds} FROM {table} '
        sql = sql_base + crit if crit else sql_base
        cur = self._execute(sql, vals)
        results = cur.fetchall()
        if commit:
            self.commit()
        return results

    def select(self,
               table: str,
               fields: List[str],
               criteria: str = None,
               values: List[Any] = None,
               commit: bool = True
               ) -> List[dict]:
        results = self.select_list(table, fields, criteria, values, commit)
        return [self._row_to_dict(fields, r) for r in results]

    def gen_select(self,
                   table: str,
                   fields: List[str],
                   criteria: str = None,
                   values: List[Any] = None,
                   commit: bool = True
                   ) -> Iterator[dict]:
        results = self.select_list(table, fields, criteria, values, commit)
        return (self._row_to_dict(fields, r) for r in results)

