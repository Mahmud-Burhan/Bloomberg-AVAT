# Bloomberg-AVAT
AVAT (Average Volume at Time) function inspired from Bloomberg Terminal to guide traders assessing recent momentum or liquidity from volume analysis.
The example product (AVAT graph) can be seen in the example.png, it only took approximately 1 second to produce 1 AVAT graph.

## Libraries required
- Jupyter Notebook
- Numpy
- Matplotlib
- Pandas
- yfinance

## How to use the project
1. This project is made as simple as possible as it is intended for personal usage.
2. The source code is made to be ran basically inside a Jupyter Notebook, which will then produce AVAT graphs.
3. Any valid stocks' ticker from yfinance API could be used, and interval days range are valid from 1-730 (depends on yfinance interval API).
4. These AVAT graphs can then be consumed to help with investment decisions (this is not a financial advice).

## Credits and links
- Inspired from: [Bloomberg](https://www.bloomberg.com/uk)
- AVAT link: [Bloomberg Trading Analytics](https://data.bloomberglp.com/professional/sites/10/2-Trading-analytics.pdf)
- yfinance API interval guides: [QMR.AI](https://www.qmr.ai/yfinance-library-the-definitive-guide/)
- Formula: [Relative Change](https://en.wikipedia.org/wiki/Relative_change)
