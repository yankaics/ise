#encoding=utf-8
ascii = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',\
	'0','1','2','3','4','5','6','7','8','9']
jump = ['~','!','@','#','$','%','^','&','*','(',')','_','+','-','=','<','>','?','/','\\','|','[',']','{','}',\
	' ',':',';','.',',','"',"'",u'·',u'…',u'，',u'。',u'！',u'“',u'”',u'《',u'》',u'？',u'（',u'）',u'：',u'；',u'、']
index = {}
#根据内容构建索引
def build(content, page_id):
	content = content.lower()
	c = len(content)
	s = 0
	#word类型 1为中文 0为英文
	t = 1
	word = ''
	for i in range(c):
		word = word.strip()
		k = content[s : s + 1]
		#如果是中文
		if k not in ascii:
			#遇到跳跃符号
			if k in jump:
				if len(word) > 1:
					record(word, s - len(word))
					word = ''
			else:
				if t == 0:
					record(word, s - len(word))
					word = k
					t = 1
				else:
					if word != '':
						record(word + k, s - len(word))
					word = k
		#如果是英文
		else:
			if t == 1:
				word = k
				t = 0
			else:
				word = word + k
		s = s + 1
	if word != '' and len(word) > 1:
		record(word, s - len(word))
	#打印全部索引
	for k in index.keys():
		print page_id,'#',k,'-',index[k]
	print len(index)

def record(keyword, s):
	if len(keyword.strip()) > 1:
		if index.has_key(keyword):
			index[keyword] = index[keyword] + ',' + str(s)
		else:
			index[keyword] = str(s)
		#print keyword, ' - ', s