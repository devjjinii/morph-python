from flask import Flask, render_template, jsonify, request
from pynori.korean_analyzer import KoreanAnalyzer
from konlpy.tag import Kkma          #Mecab
from konlpy.utils import pprint
from flask_cors import CORS


# @author : jin

app = Flask(__name__)
# 인코딩
app.config['JSON_AS_ASCII'] = False
# cors오류
CORS(app)


@app.route('/', methods=['GET'])
def index():
    data = {'name' : 'jin'}
    return jsonify(data)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/pynori')
def pynori():
    # value = request.form['pynori_tag']
    value = request.args.get('search')

    # nori = KoreanAnalyzer(decompound_mode='MIXED',
    #                   infl_decompound_mode='DISCARD',
    #                   discard_punctuation=True,
    #                   output_unknown_unigrams=False,
    #                   pos_filter=False, stop_tags=['JKS', 'JKB', 'VV', 'EF'])

    # 필터링되는 POS 태그 리스트 (pos_filter=True일 때만 활성)
   
    result = nori.do_analysis(value)
   
    print(result)
    print(result['termAtt'])
    # lang = jsonify(result)
    # print(lang)

    return result

# 서버를 띄울때 미리 로딩해 놓는다. -> 속도가 느리다.
def noriInit():
    global nori
    nori = KoreanAnalyzer(decompound_mode='MIXED',
                    infl_decompound_mode='DISCARD',
                    discard_punctuation=True,
                    output_unknown_unigrams=False,
                    pos_filter=False, stop_tags=['JKS', 'JKB', 'VV', 'EF'])   

@app.route('/konlpy')
def konlpy():

    # value = request.form['konlpy_tag']
    value = request.args.get('search')

    kkma = Kkma()
    
    a = kkma.pos(value)
    noun = kkma.nouns(value)
    
    word = []
    pos = []

    for i in a:
        # print(i[0] + ',' + i[1])
        word.append(i[0])
        pos.append(i[1])

    print(noun)
    print(word)
    print(pos)
   
    result =  {'word': word , 'pos': pos , 'noun': noun }
    print(result)

    return result

if __name__ == "__main__":
    noriInit()
    app.run(host='0.0.0.0', port='5000', debug=True)