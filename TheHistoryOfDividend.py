import yfinance as yf
import argparse
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_dividends(etf_ticker, months=12):
    try:
        # Ticker 객체 생성
        etf = yf.Ticker(etf_ticker)

        # 분배금(배당금) 데이터 가져오기
        dividends = etf.dividends

        # 이번 달 기준 기간 계산
        today = datetime.today()
        first_day_of_this_month = today.replace(day=1)
        start_date = first_day_of_this_month - timedelta(days=(months - 1) * 30)

        # 기간 필터링
        dividends = dividends[start_date.strftime('%Y-%m-%d'):today.strftime('%Y-%m-%d')]

        if dividends.empty:
            print(f"No dividend information found for {etf_ticker}. (Period: {start_date.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')})")
        else:
            print(f"Dividend information for {etf_ticker} ({start_date.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}):")
            print(dividends)

            # 평균 값 계산
            average_dividend = dividends.mean()

            # 차트 그리기
            plt.figure(figsize=(10, 6))
            plt.plot(dividends.index.strftime('%Y-%m-%d'), dividends.values, marker='o', linestyle='-', label="Dividends")

            # 평균선 추가
            plt.axhline(y=average_dividend, color='r', linestyle='--', label=f"Average: {average_dividend:.3f}")

            # 값 표시
            for i, value in enumerate(dividends.values):
                plt.text(dividends.index[i].strftime('%Y-%m-%d'), value, f'{value:.3f}', ha='center', va='bottom', fontsize=9)

            plt.title(f"{etf_ticker} Dividends ({start_date.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')})")
            plt.xlabel("Date")
            plt.ylabel("Dividends")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve ETF dividend information.")
    parser.add_argument("ticker", type=str, help="Ticker symbol of the ETF to query")
    parser.add_argument("months", type=int, nargs="?", default=12, help="Number of months to query data from (default: 12)")
    args = parser.parse_args()

    get_dividends(args.ticker, args.months)
