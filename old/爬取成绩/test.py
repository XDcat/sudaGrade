from pprint import pprint
import json
with open('C:\\Users\S\Desktop\爬取成绩\\all_student_grade_2017.txt','r') as f:
    for i in f:
        temp = json.loads(i)
        pprint(temp)