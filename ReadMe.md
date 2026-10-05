# US Options Dashboard — Analysis & Paper Trading

A lightweight, single-page web application (SPA) for analyzing US equity options, scanning for technical confluence, and executing simulated paper trades. Built entirely in vanilla HTML, CSS, and JavaScript, this dashboard requires no database or backend installation and runs entirely in the browser using `localStorage` for data persistence.

## Core Features

* **Automated Options Screener:** Scans a customizable watchlist (e.g., NVDA, SPY, QQQ, AAPL) for options setups based on technical indicators (EMA, MACD, RSI, VWAP) across 5-minute and 15-minute timeframes.
* **Smart Strike Selection:** Automatically filters the options chain for contracts that meet strict liquidity, open interest, bid/ask spread, and Greek (Delta) criteria.
* **Dynamic Risk Management:** Calculates Stop Loss (SL) and Take Profit (TP) levels dynamically using Average True Range (ATR) multiples and option Greeks (Delta and Gamma approximations).
* **Paper Trading Engine:** Complete simulated trading environment supporting customizable entry quantities, automated commission fee deduction (e.g., Moomoo standard $0.65/contract), and real-time unrealized/realized P&L tracking.
* **Direct Broker Integration:** One-click redirection to exact option contract charts on Moomoo, TradingView, or Yahoo Finance.
* **Trade Journaling:** Logs all closed paper trades with performance metrics (Win Rate, Profit Factor, Largest Win/Loss) and supports exporting to CSV or JSON.

## Setup & Installation

This application requires no build tools or package managers.

1. Download or save the `index.html` file.
2. Double-click the file to open it in any modern web browser (Chrome, Edge, Firefox, Safari).
3. Navigate to the **DATA SOURCES** tab to configure your market data connection.

## Data Providers

The dashboard requires live or delayed market data to generate signals. It supports three modes:

1. **Polygon / Massive:** Direct browser API connection. Requires a Polygon.io API key with an options data subscription.
2. **Moomoo (via Custom Proxy):** Connects to Moomoo's OpenD gateway. Because OpenD uses a local TCP/protobuf protocol, you must run a lightweight proxy server that exposes REST endpoints (`/bars` and `/chain`) with CORS enabled to communicate with the browser.
3. **Demo / Simulated Mode:** A built-in, math-driven simulator that generates realistic price action, Greeks, and option chains for UI testing and weekend practice when markets are closed.

## Application Modules (Tabs)

* **Overview:** Displays high-level market context, broad regime status (Bullish/Bearish/Neutral), and technical performance of major indices (SPY, QQQ, IWM, DIA).
* **Auto-Picks:** The core screener. Displays qualified Call and Put setups scored out of 100 based on momentum, trend, liquidity, and implied volatility (IV). Includes a breakdown of rejected tickers.
* **Options Chain:** A simplified, tabular view of the current options chain for any watched ticker, highlighting the At-The-Money (ATM) strikes and top volume contracts.
* **Technical Analysis:** A detailed breakdown of the underlying technical data (RSI, ATR, MACD Histogram, Relative Volume) for all tickers in the watchlist.
* **Paper Trading:** Manage open positions, edit contract quantities on the fly, and view aggregate portfolio performance. Includes options to clear historical data.
* **Settings:** Fine-tune the algorithmic logic. Adjust target ATR multiples, delta ranges, maximum capital risk, contract commission fees, and default chart providers.

## Security & Privacy

* **Local Execution:** All calculations, screening, and logic occur client-side in your browser.
* **Data Storage:** Watchlists, paper trades, and settings are stored locally in the browser's `localStorage`. Clearing your browser data will wipe your trading journal.
* **API Keys:** API keys and proxy secrets are held in memory only for the duration of the session and are stored locally. They are never sent to third-party servers (other than your configured data providers).

## Disclaimer

**For educational and analysis purposes only.** This tool is a paper-trading simulator and screener. It cannot execute real orders. The technical confluence scores provided are rule-based mathematical probabilities, not financial advice or guaranteed indicators of profit. Trading options involves significant risk of loss.