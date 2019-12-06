import docx2txt
import re
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
text = docx2txt.process("/Users/bahrami-a/Desktop/exam.docx", "/Users/bahrami-a/Desktop/tmp/")
text = text.replace("\u3000", " ")
# text = text.replace("\n","")
text = text.split("\n")
quiz = {}
keys = []
current_question = []
image_index = 1
def parse_question(question, img_index):
    question = list(filter(None, question)) # remove empty string created by split()
    question_data_format = [question[0]]
    for index in range(len(question)):
        if "選択肢" in question[index]:
            question_data_format.append(":")
            multiselection = question[index - 2]
            multiselection += question[index - 1]
            multiselection = "".join(multiselection.split())
            multiselection = multiselection.replace(" ", "")
            multiselection = multiselection.split("）")
            multiselection = list(filter(None, multiselection)) # remove empty string created by split()

            multiselection[0], multiselection[1], multiselection[2], multiselection[3] = multiselection[0] + (f")image{img_index+1}"), multiselection[1] + (f")image{img_index}"), multiselection[2] + (f")image{img_index+3}"), multiselection[3] + (f")image{img_index+2}")
            img_index += 4
            question_data_format.append(",".join(multiselection))
            question_data_format.append(":")
            answer = ",".join(question[index+1].replace("）", ")").split())
            question_data_format.append(answer)
    return "".join(question_data_format), img_index


for index, text_line in enumerate(text):
    if text_line is not "" :
        text_line = " ".join(text_line.split())
        if re.search("^第.*問", text_line):
            print()
            while "答え" not in text[index] and index + 1 < len(text):
                index += 1
                if text[index] is not "" and "答え" not in text[index]:
                    question = text[index].split()
                    question = " ".join(question)
                    current_question.append(question)
                elif text[index] is not "" and "答え" in text[index]:
                    answer = text[index].split()
                    if "〇" in answer:
                        answer = "true"
                    elif "×" in answer:
                        answer = "false"
                    else:
                        answer = answer[1]
                    question, image_index = parse_question(current_question, image_index)
                    # print(current_question)
                    quiz[question] = answer
                    current_question = []

from filemanager import FileManager

fm = FileManager()
Exam = {"key1":quiz}
fm.save_to_json(Exam)
#
# 本会の「安心Ｒ住宅　住宅リフォーム工事実施判断チェックシート」関して、以下の既存住宅の外壁について明らかに不具合事象と判定される事象の組み合わせはどれか。
# イ）　　　　　　　　　　　　　　　　　　　　ロ）
#
# ハ）　　　　　　　　　　　　　　　　　　　ニ）
#
#
# 選択肢
# ａ）イとロとニ　  b）イとニ　　c）イとハとニ　 d) イとロ

# "question:イ)image2,ロ）image1,ハ）image4,ニ）image3:a)イとロ"
