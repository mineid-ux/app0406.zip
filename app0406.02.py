import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform


# 한글 폰트 설정 함수
def set_korean_font():
    system_name = platform.system()
    if system_name == "Windows":
        plt.rc('font', family='Malgun Gothic')
    elif system_name == "Darwin":  # Mac
        plt.rc('font', family='AppleGothic')
    else:  # Linux
        plt.rc('font', family='NanumGothic')
    plt.rc('axes', unicode_minus=False)


# 데이터 로드 함수
def load_data(file):
    return pd.read_csv(file)


# 산점도 그래프 생성 및 출력 함수
def display_scatter_plot(df, x_col, y_col, hue_col, show_reg):
    fig, ax = plt.subplots(figsize=(10, 6))

    if show_reg:
        # 추세선(회귀선) 및 산점도 시각화
        sns.regplot(data=df, x=x_col, y=y_col, ax=ax, scatter=False, color='red')

    # 범주별 색상 구분을 포함한 산점도
    sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col, ax=ax, s=100)

    ax.set_title(f"{x_col}와(과) {y_col}의 관계 (Scatter Plot)")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig)


# 메인 실행 함수
def main():
    st.title("산점도 그래프로 데이터 비교")
    set_korean_font()

    # 1. 파일 업로드
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # 2. 데이터 확인
        st.subheader("데이터 확인")
        st.write(df.head())

        # 3. 비교 항목 선택
        st.subheader("비교 항목 선택")
        cols = df.columns.tolist()
        num_cols = df.select_dtypes(include=['number']).columns.tolist()

        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X축(설명 변수) 선택", num_cols)
        with col2:
            y_axis = st.selectbox("Y축(반응 변수) 선택", num_cols)

        hue_axis = st.selectbox("색상으로 구분할 범주 컬럼(선택)", [None] + cols)
        show_reg = st.checkbox("추세선(회귀선) 표시", value=True)

        # 4. 그래프 생성 버튼 및 시각화
        if st.button("그래프 생성"):
            display_scatter_plot(df, x_axis, y_axis, hue_axis, show_reg)


if __name__ == "__main__":
    main()