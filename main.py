import streamlit as st

# --- ページ設定 ---
st.set_page_config(layout="centered", page_title="MindTrace")

# --- ページ遷移用関数 ---
def next_step(current_q_key, radio_key, next_step_num):
    """ラジオボタンが押された瞬間に実行される関数"""
    # 選択された値を保存用のキーにコピー
    st.session_state[current_q_key] = st.session_state[radio_key]
    # ステップを進める
    st.session_state.step = next_step_num

# --- CSS ---
st.markdown("""
<style>
body { background-color: #F3EFE8; }
.block-container { max-width: 700px; padding-top: 0rem; }
.header {
    background-color: #1E1B6A; padding: 60px 20px;
    border-bottom-left-radius: 50px; border-bottom-right-radius: 50px;
    text-align: center; color: white; font-size: 28px; font-weight: bold;
}
.title {
    font-size: 35px;
    font-weight: bold;
}

.subtitle {
    font-size: 20px;
    margin-top: 8px;
    opacity: 0.8;
}
div.stButton > button {
    background-color: #1E1B6A; color: white; border-radius: 30px;
    height: 3em; width: 200px; font-size: 16px; display: block; margin: 40px auto 0 auto;
}
div[role="radiogroup"] > label {
    display: flex !important; align-items: center !important; gap: 10px;
    background-color: white; padding: 14px 16px; border-radius: 12px;
    border: 1px solid #ddd; cursor: pointer; margin-bottom: 10px;
}
div[role="radiogroup"] input[type="radio"] { margin: 0; transform: scale(1.2); }
div[role="radiogroup"] > label:has(input:checked) {
    border: 2px solid #1E1B6A; background-color: #F7F8FF;
}
div[role="radiogroup"] > label:hover { border: 1px solid #1E1B6A; }
.q-circle {
    display: inline-block; width: 35px; height: 35px; background-color: #1E1B6A;
    color: white; border-radius: 50%; text-align: center; line-height: 35px;
    font-weight: bold; margin-right: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- マッピングデータ ---
q2_map = {
    "照明が落ちることがどういう状態かを考える": {
        "label": "本質的な原因から状況を理解しようとする",
        "function": "Ni",
        "mbti": ["INTJ", "INFJ"],
        "desc": "物事の裏にある構造や因果関係を読み取ろうとする思考"
    },
    "入力から出力までの配線のルートを思い出す": {
        "label": "仕組みや構造を分解して考える",
        "function": "Ti",
        "mbti": ["INTP", "ISTP"],
        "desc": "システムのロジックや構造を正確に理解しようとする思考"
    },
    "照明に関連する機材や配線をすべて考える": {
        "label": "可能性を広げて全体像を捉える",
        "function": "Ne",
        "mbti": ["ENTP", "ENFP"],
        "desc": "あらゆる可能性を広げてパターンを探る思考"
    },
    "この手のトラブルで一番多かったケースを思い出す": {
        "label": "過去の経験や前例をもとに判断する",
        "function": "Si",
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "過去のデータや経験を基準に判断する思考"
    },

    "照明がつかないまま音楽だけ流れる状態が映像で流れる": {
        "label": "未来の展開や最悪のシナリオを想像する",
        "function": "Ni",
        "mbti": ["INTJ", "INFJ"],
        "desc": "未来の流れや結果を先読みする思考"
    },
    "焦りすぎて気が気じゃない人がいないかを心配する": {
        "label": "周囲の人の感情や状態を気にかける",
        "function": "Fe",
        "mbti": ["ENFJ", "ESFJ"],
        "desc": "場の空気や他者の感情を優先する思考"
    },
    "ライブが盛り上がらず次回の集客力が減ることを心配する": {
        "label": "成果や結果への影響を考える",
        "function": "Te",
        "mbti": ["ENTJ", "ESTJ"],
        "desc": "結果や効率を最優先に考える思考"
    },
    "照明トラブルでどんな事例起きたか思い出す": {
        "label": "過去の事例からパターンを探す",
        "function": "Si",
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "既存の事例をベースに判断する思考"
    },

    "どうすれば最もマシになるか": {
        "label": "現実的な最適解を探そうとする",
        "function": "Te",
        "mbti": ["ENTJ", "ESTJ"],
        "desc": "現実ベースで最も効率の良い解を選ぶ思考"
    },
    "具体的にどこがトラブっているのか": {
        "label": "現場の状況を正確に把握しようとする",
        "function": "Se",
        "mbti": ["ESTP", "ESFP"],
        "desc": "今この瞬間の現実を正確に捉える思考"
    },
    "何か代わりになるものはないか": {
        "label": "代替案や別の可能性を考える",
        "function": "Ne",
        "mbti": ["ENTP", "ENFP"],
        "desc": "柔軟に別の選択肢を発想する思考"
    },
    "どんな解決策が使えるか": {
        "label": "使える手段を整理して考える",
        "function": "Te",
        "mbti": ["ENTJ", "ESTJ"],
        "desc": "実行可能な手段を整理して選ぶ思考"
    },

    "失敗して気分が落ち込む人がたくさん出てしまうことを防ぎたい": {
        "label": "人への影響を最小化しようとする",
        "function": "Fe",
        "mbti": ["ENFJ", "ESFJ"],
        "desc": "周囲の感情への影響を最優先する思考"
    },
    "せっかく頑張ってきたイベントを台無しにしたくない": {
        "label": "自分の価値や努力を守ろうとする",
        "function": "Fi",
        "mbti": ["INFP", "ISFP"],
        "desc": "自分の信念や価値を守る思考"
    },
    "何も考えが浮かんでないけど気づいたら動いてる": {
        "label": "直感的に体を動かして対応する",
        "function": "Se",
        "mbti": ["ESTP", "ESFP"],
        "desc": "考えるより先に行動するタイプ"
    },
    "トラブルがハラハラしすぎてさっさと解決したい": {
        "label": "不安を解消するために早く安定させたい",
        "function": "Si",
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "安定状態に戻すことを優先する思考"
    }
}
q3_map = {
    "この場を成立させるための措置をする": {
        "label": "状況を維持するための現実的な判断をする",
        "function": "Se",
        "mbti": ["ESTP", "ESFP"],
        "desc": "今この瞬間を成立させることを最優先にする現場型判断"
    },
    "解決に直結するものを選ぶ": {
        "label": "最も効率よく結果に繋がる選択をする",
        "function": "Ti",
        "mbti": ["INTP", "ISTP"],
        "desc": "論理的に最短ルートで問題解決する思考"
    },
    "最もマシで済む措置を実行する": {
        "label": "損失を最小限に抑える判断をする",
        "function": "Te",
        "mbti": ["ENTJ", "ESTJ"],
        "desc": "現実的に被害を最小化する合理的判断"
    },
    "トラブルの本質解消に繋がるものを選ぶ": {
        "label": "根本的な問題解決を優先する",
        "function": "Ni",
        "mbti": ["INTJ", "INFJ"],
        "desc": "表面的ではなく原因レベルで解決しようとする思考"
    },
    "複数の可能性を考慮して一番期待値の高いものを選ぶ": {
        "label": "選択肢を比較して最適な未来を選ぶ",
        "function": "Ne",
        "mbti": ["ENTP", "ENFP"],
        "desc": "複数の未来を比較して最も可能性の高いものを選ぶ思考"
    },
    "周囲の影響や空気に沿って決めるor従う": {
        "label": "周囲との調和を重視して判断する",
        "function": "Fe",
        "mbti": ["ENFJ", "ESFJ"],
        "desc": "場の空気や人間関係を優先した意思決定"
    },
    "自分で納得の行く方法で試してみる": {
        "label": "自分の価値観や納得感で決める",
        "function": "Fi",
        "mbti": ["INFP", "ISFP"],
        "desc": "自分の中の信念や納得を基準に動く思考"
    },
    "確実に安全で結果が予想できる策を実行する": {
        "label": "安定性と再現性を重視する",
        "function": "Si",
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "確実性と過去の再現性を重視する判断"
    }
}
q4_map = {
    "『お前はこれやれ！』って即座に役割振る": {
        "label": "周囲に指示を出して全体を動かす",
        "function": "Te",
        "mbti": ["ENTJ", "ESTJ"],
        "desc": "全体最適のために人を動かすリーダー型行動"
    },
    "考える前に現場に走って触る": {
        "label": "自分で現場に入り直接対応する",
        "function": "Se",
        "mbti": ["ESTP", "ESFP"],
        "desc": "状況を体感しながら即座に行動するタイプ"
    },
    "周囲の喧騒をシャットアウトして頭の中で構造を組み立てる": {
        "label": "思考に集中して問題を整理する",
        "function": "Ti",
        "mbti": ["INTP", "ISTP"],
        "desc": "外界を遮断して論理的に構造を組み立てる"
    },
    "『みんな落ち着いて！』って空気を整えにいく": {
        "label": "場の雰囲気を整えて混乱を抑える",
        "function": "Fe",
        "mbti": ["ENFJ", "ESFJ"],
        "desc": "人の感情や空気を整えることで状況を安定させる"
    },
    "その場で代替案をいくつも思いついて試そうとする": {
        "label": "柔軟にアイデアを出して試行する",
        "function": "Ne",
        "mbti": ["ENTP", "ENFP"],
        "desc": "思いついた選択肢をどんどん試す発散型行動"
    },
    "一旦止めて安全確保や手順確認を優先する": {
        "label": "リスクを抑えながら慎重に進める",
        "function": "Si",
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "安全性と手順を守ることで安定した対応をする"
    },
    "全体の流れや原因を抽象的に把握しようとする": {
        "label": "全体構造を俯瞰して理解する",
        "function": "Ni",
        "mbti": ["INTJ", "INFJ"],
        "desc": "表面的ではなく全体の流れを抽象的に捉える"
    },
    "自分の中の違和感や直感に従って動く": {
        "label": "直感や内面的な感覚で動く",
        "function": "Fi",
        "mbti": ["INFP", "ISFP"],
        "desc": "論理よりも内面的な感覚や違和感を重視する"
    }
}
q5_map = {
    "バレずに乗り切れたら普通に満足": {
        "label": "その場を乗り切れたかどうかを重視する",
        "function": "Se",
        "mbti": ["ESTP", "ESFP"],
        "desc": "結果よりも今を乗り切れたかを重視する"
    },
    "結果として成功ラインに戻せたらOK": {
        "label": "成果や目標達成を基準にする",
        "function": "Te",
        "mbti": ["ENTJ", "ESTJ"],
        "desc": "最終的な結果や成果で評価する思考"
    },
    "原因を特定できた時点で満足": {
        "label": "問題の理解や特定に価値を感じる",
        "function": "Ti",
        "mbti": ["INTP", "ISTP"],
        "desc": "構造や原因を理解できたこと自体に価値を感じる"
    },
    "もう二度と起きない仕組みにできたら満足": {
        "label": "再発防止や構造改善を重視する",
        "function": "Ni",
        "mbti": ["INTJ", "INFJ"],
        "desc": "未来に同じ問題が起きない構造を作る思考"
    },
    "関係者が納得して終われたら満足": {
        "label": "人の納得や関係性を大事にする",
        "function": "Fe",
        "mbti": ["ENFJ", "ESFJ"],
        "desc": "関係者全員の感情的な納得を重視する"
    },
    "自分的に納得いくやり方ができたら満足": {
        "label": "自分の価値観に沿えたかを重視する",
        "function": "Fi",
        "mbti": ["INFP", "ISFP"],
        "desc": "自分の信念や納得感を最優先する"
    },
    "もっと良いやり方の可能性が見えたら満足": {
        "label": "可能性や改善余地を見出すことに価値を感じる",
        "function": "Ne",
        "mbti": ["ENTP", "ENFP"],
        "desc": "新しい可能性や発展性に価値を感じる"
    },
    "安定した形に戻せたら安心する": {
        "label": "安定した状態に戻ることを重視する",
        "function": "Si",
        "mbti": ["ISTJ", "ISFJ"],
        "desc": "安心できる既存の状態に戻ることを重視する"
    }
}
# --- 初期化 ---
for key in ["q1","q2","q3","q4","q5"]:
    if key not in st.session_state:
        st.session_state[key] = None

if "step" not in st.session_state:
    st.session_state.step = 1

# --- メインコンテンツ ---
st.markdown('''
<div class="header">
    <div class="title">MindTrace</div>
    <div class="subtitle">あなたの“意思決定”、可視化してみる？</div>
</div>
''', unsafe_allow_html=True)

# 診断中は共通の導入文を表示（必要なければif文の中へ移動してください）
if st.session_state.step <= 5:
    st.markdown("## 大問1")
    st.markdown("あなたはライブ会場の現場スタッフです。機材トラブルが起きて、照明がつかなくなったことをインカムから知らされました。")

# --- 各ステップの表示 ---
if st.session_state.step == 1:
    st.markdown('<div style="display:flex; align-items:center;"><div class="q-circle">1</div><div style="font-weight:700;">その情報を聞いた瞬間、あなたは何を考えると思いますか？</div></div>', unsafe_allow_html=True)
    st.radio("", [
        "なぜ照明がつかなくなったのか？", "ライブが失敗してしまうのではないか？",
        "どうやって乗り切るべきか", "はやくなんとかしないと"
    ], key="radio_q1", index=None, on_change=next_step, args=("q1", "radio_q1", 2))

elif st.session_state.step == 2:
    q1 = st.session_state.q1
    if q1 == "なぜ照明がつかなくなったのか？":
        title, options = "あなたはどのように予想を立てると思いますか？", ["照明が落ちることがどういう状態かを考える", "入力から出力までの配線のルートを思い出す", "照明に関連する機材や配線をすべて考える", "この手のトラブルで一番多かったケースを思い出す"]
    elif q1 == "ライブが失敗してしまうのではないか？":
        title, options = "どのようなケースを想像しますか？", ["照明がつかないまま音楽だけ流れる状態が映像で流れる", "焦りすぎて気が気じゃない人がいないかを心配する", "ライブが盛り上がらず次回の集客力が減ることを心配する", "照明トラブルでどんな事例起きたか思い出す"]
    elif q1 == "どうやって乗り切るべきか":
        title, options = "解決にあたって着目する点はどこですか？", ["どうすれば最もマシになるか", "具体的にどこがトラブっているのか", "何か代わりになるものはないか", "どんな解決策が使えるか"]
    else:
        title, options = "どういう思いで焦ると思いますか？", ["失敗して気分が落ち込む人がたくさん出てしまうことを防ぎたい", "せっかく頑張ってきたイベントを台無しにしたくない", "何も考えが浮かんでないけど気づいたら動いてる", "トラブルがハラハラしすぎてさっさと解決したい"]

    st.markdown(f'<div style="display:flex; align-items:center;"><div class="q-circle">2</div><div style="font-weight:700;">{title}</div></div>', unsafe_allow_html=True)
    st.radio("", options, key="radio_q2", index=None, on_change=next_step, args=("q2", "radio_q2", 3))

elif st.session_state.step == 3:
    st.markdown('<div style="display:flex; align-items:center;"><div class="q-circle">3</div><div style="font-weight:700;">最終的にあなたはどのような決断をすると思いますか？</div></div>', unsafe_allow_html=True)
    st.radio("", [
        "この場を成立させるための措置をする", "解決に直結するものを選ぶ", "最もマシで済む措置を実行する", "トラブルの本質解消に繋がるものを選ぶ",
        "複数の可能性を考慮して一番期待値の高いものを選ぶ", "周囲の影響や空気に沿って決めるor従う", "自分で納得の行く方法で試してみる", "確実に安全で結果が予想できる策を実行する"
    ], key="radio_q3", index=None, on_change=next_step, args=("q3", "radio_q3", 4))

elif st.session_state.step == 4:
    st.markdown('<div style="display:flex; align-items:center;"><div class="q-circle">4</div><div style="font-weight:700;">その判断のもと、あなたはどう動きますか？</div></div>', unsafe_allow_html=True)
    st.radio("", [
        "『お前はこれやれ！』って即座に役割振る", "考える前に現場に走って触る", "周囲の喧騒をシャットアウトして頭の中で構造を組み立てる", "『みんな落ち着いて！』って空気を整えにいく",
        "その場で代替案をいくつも思いついて試そうとする", "一旦止めて安全確保や手順確認を優先する", "全体の流れや原因を抽象的に把握しようとする", "自分の中の違和感や直感に従って動く"
    ], key="radio_q4", index=None, on_change=next_step, args=("q4", "radio_q4", 5))

elif st.session_state.step == 5:
    st.markdown('<div style="display:flex; align-items:center;"><div class="q-circle">5</div><div style="font-weight:700;">その後、あなたは何に納得しますか？</div></div>', unsafe_allow_html=True)
    st.radio("", [
        "バレずに乗り切れたら普通に満足", "結果として成功ラインに戻せたらOK", "原因を特定できた時点で満足", "もう二度と起きない仕組みにできたら満足",
        "関係者が納得して終われたら満足", "自分的に納得いくやり方ができたら満足", "もっと良いやり方の可能性が見えたら満足", "安定した形に戻せたら安心する"
    ], key="radio_q5", index=None, on_change=next_step, args=("q5", "radio_q5", 6))

# --- 結果表示 ---
elif st.session_state.step == 6:

    st.markdown("""
    <style>

    /* 結果コンテナ（影消す＆フラット） */
    .result-container {
        background-color: transparent;
        padding: 20px 10px;
        margin-top: 30px;
    }

    /* タイトル */
    .result-title {
        color: #1E1B6A;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* 各ブロック */
    .result-block {
        margin-bottom: 28px;
    }

    /* 見出し */
    .result-heading {
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 8px;
    }

    /* 本文 */
    .result-text {
        color: #333;
        padding-left: 14px;
        line-height: 1.7;
    }

    /* 青丸アイコン */
    .blue-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #1E1B6A;
        border-radius: 50%;
        margin-right: 8px;
    }

    /* セクションタイトル */
    .section-title {
        margin-top: 35px;
        font-weight: 700;
        color: #1E1B6A;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="result-container">', unsafe_allow_html=True)

    st.markdown('<div class="result-title">診断結果</div>', unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom:25px;'>あなたはトラブルに直面したとき、</p>", unsafe_allow_html=True)
    
    # --- ブロック表示関数 ---
    def render_block(title, data):

        label = data.get("label","")
        function = data.get("function","")
        mbti = ", ".join(data.get("mbti",[]))
        desc = data.get("desc","")

        st.markdown(f"""
        <div class="result-block">
        <div class="result-heading">{title}</div>

        <div class="result-text">→ {label}</div>

        <div class="result-text">
        <span class="blue-dot"></span>認知機能：{function}<br>
        <span class="blue-dot"></span>MBTI候補：{mbti}<br>
        <span class="blue-dot"></span>{desc}
        </div>

        </div>
        """, unsafe_allow_html=True)
    
    # --- 各ブロック ---
    data2 = q2_map.get(st.session_state.q2, {})
    data3 = q3_map.get(st.session_state.q3, {})
    data4 = q4_map.get(st.session_state.q4, {})
    data5 = q5_map.get(st.session_state.q5, {})

    render_block("① 状況の捉え方", data2)
    render_block("② 意思決定", data3)
    render_block("③ 行動パターン", data4)
    render_block("④ 納得基準", data5)

    # --- 認知機能まとめ ---
    functions = []
    mbti_candidates = []

    for data in [data2, data3, data4, data5]:
        if data:
            f = data.get("function")
            if f:
                functions.append(f)
            mbti_candidates += data.get("mbti", [])

    st.markdown('<div class="section-title">認知パターン</div>', unsafe_allow_html=True)

    if functions:
        st.markdown("・" + "<br>・".join(functions), unsafe_allow_html=True)

    # --- MBTI候補 ---
    st.markdown('<div class="section-title">MBTI候補</div>', unsafe_allow_html=True)

    if mbti_candidates:
        st.markdown("→ " + " / ".join(mbti_candidates[:3]))

    # --- 注釈 ---
    st.markdown("""
    <div style="margin-top:30px; font-size:13px; color:#666;">
    ※これは性格を決めつけるものではなく、意思決定の傾向を可視化したものです
    </div>
    """, unsafe_allow_html=True)

    # --- リセット ---
    if st.button("もう一度診断する"):
        for key in ["q1","q2","q3","q4","q5"]:
            st.session_state[key] = None
        st.session_state.step = 1
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)