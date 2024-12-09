"""
$ python ./CurrencyRates.py
"""
import datetime
import statistics
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_exchange_rates(retries=3):
    # 현재 날짜와 3년 전 날짜 계산
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=3*365)

    for attempt in range(retries):
        try:
            logging.info(f"환율 데이터를 가져오는 중... 시도 {attempt + 1}/{retries}")
            # Yahoo Finance에서 원/달러 환율 데이터 다운로드
            data = yf.download('KRW=X', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

            # 데이터 내용 로깅
            logging.info(f"가져온 데이터 샘플: \n{data.head()}")
            logging.info(f"데이터 열 이름: {data.columns}")

            # 'Adj Close' 열에서 환율 데이터 추출
            if isinstance(data, pd.DataFrame) and ('Adj Close', 'KRW=X') in data.columns:
                rates = data[('Adj Close', 'KRW=X')].dropna().astype(float)
                if not rates.empty:
                    logging.info("환율 데이터를 성공적으로 가져왔습니다.")
                    return rates
                else:
                    logging.warning(f"데이터가 비어 있습니다. 다시 시도합니다... 가져온 데이터: \n{data}")
            else:
                logging.warning(f"올바른 데이터를 가져오지 못했습니다. 다시 시도합니다... 가져온 데이터: \n{data}")
        except Exception as e:
            logging.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}. 다시 시도합니다...")
        time.sleep(2)  # 재시도 전에 2초 대기

    # 모든 시도 실패 시 빈 Series 반환
    logging.error("모든 시도에서 환율 데이터를 가져오는 데 실패했습니다.")
    return pd.Series(dtype='float64')

def calculate_average_rate(rates):
    # 평균 환율 계산 (숫자만 포함하도록 필터링)
    numeric_rates = pd.to_numeric(rates, errors='coerce').dropna()
    logging.info(f"필터링된 유효한 데이터 포인트 수: {len(numeric_rates)}")
    if len(numeric_rates) > 0:
        average_rate = statistics.mean(numeric_rates)
        logging.info(f"최근 3년간 원/달러 평균 환율: {average_rate:.2f} KRW/USD")
        return average_rate
    else:
        logging.warning("유효한 환율 데이터가 없습니다.")
        return None

def plot_exchange_rates(rates, average_rate):
    # 환율 데이터 시각화
    plt.figure(figsize=(10, 5))
    plt.plot(rates.index, rates.values, label='KRW/USD Exchange Rate', color='blue')
    plt.axhline(y=average_rate, color='red', linestyle='--', label=f'Average Rate: {average_rate:.2f} KRW/USD')
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate (KRW/USD)')
    plt.title('KRW/USD Exchange Rate Over the Last 3 Years')
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()  # X축 날짜 포맷팅
    plt.show()

if __name__ == "__main__":
    logging.info("환율 데이터 수집을 시작합니다.")
    rates = fetch_exchange_rates()
    if not rates.empty:
        average_rate = calculate_average_rate(rates)
        if average_rate is not None:
            plot_exchange_rates(rates, average_rate)
    else:
        logging.error("환율 데이터를 가져올 수 없습니다.")
