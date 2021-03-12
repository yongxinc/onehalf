class Top:
    def __init__(self, title, sizeHeaders, sizeDetailHeaders, sizeDetailInfos, hasMultiTables):
        self.title = title
        self.sizeHeaders = sizeHeaders
        self.sizeDetailHeaders = sizeDetailHeaders
        self.sizeDetailInfos = sizeDetailInfos
        self.hasMultiTables = hasMultiTables
        self.sizeTable = dict()

    def processTables(self):
        toAppend = ''

        if self.hasMultiTables:
            print('有兩個table')  # 4+...
            for k in range(4):
                for i in range(len(self.sizeHeaders)*len(self.sizeDetailHeaders)):
                    toAppend += self.sizeDetailInfos[i] + " "
                    self.sizeTable[self.sizeHeaders[k]] = toAppend
        else:
            print('只有一個table')
            # print('len(self.sizeHeaders)*len(self.sizeDetailHeaders) : ' +
            #       str(len(self.sizeHeaders)*len(self.sizeDetailHeaders)))
            # print(len(self.sizeDetailInfos))
            for k in range(len(self.sizeHeaders)):
                self.sizeTable[self.sizeHeaders[k]] = ""

        print(self.sizeTable)
