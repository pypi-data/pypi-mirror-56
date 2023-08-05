
import Orange.data
from Orange.data import Domain, ContinuousVariable
import math

class InputMixin():

    def getDomainWithUserDefinedColumns(self, userCols):
      columns = self.predefinedColumns + list(map(lambda col: ContinuousVariable.make(col), userCols))
      domain = Domain(columns, source = self.predefinedDomain, metas = self.domainMetas)
      return domain

    def getUserDefinedColumns(self, stage):
      columns = []
      if stage.get("userDefined", False):
        for col in stage["userDefined"]:
          columns.append(col)
      return columns


    def fillUserDefinedRows(self, stage, userCols, row):
      for column in userCols:
        value = math.nan
        try:
          value = float(stage.get(column, math.nan))
        except:
          pass
        row.append(value)
      return row

    def fillMetas(self, stage, metas, row):
      for column in metas:
        value = ""
        try:
          value = str(stage.get(column, ""))
        except:
          pass
        row.append(value)
      return row

    def dataReceived(self, data):
      metas = data["metas"]
      wellNames = []
      completion = []
      domain = self.predefinedDomain
      if data:
        userCols = data["columns"]
        domain = self.getDomainWithUserDefinedColumns(userCols)
        for stage in data["data"]:
          row = self.fillUserDefinedRows(stage, userCols, [])
          wellNames.append(self.fillMetas(stage, metas, []))
          completion.append(row)

      table = Orange.data.Table(domain)
      if completion:
        table = Orange.data.Table.from_numpy(domain, completion, metas=wellNames)
      print(table)
      self.table = table
      self.Outputs.data.send(self.table)

