# AlphaPulse | Pro Options Terminal & Paper Trading Dashboard

AlphaPulse is a lightweight, client-side US equities options screening and paper trading dashboard. It tracks underlying momentum indicators (EMA, RSI, HV), scans real-time or near-real-time option chains, computes Black-Scholes Greeks ($\Delta$, $\Theta$, IV), and provides an interactive paper trading portfolio with direct deep-links to Moomoo option strikes.

---

## Features

- **Automated Strike Scanner (`Auto-Picks`)**:
  - Filters high-probability single-leg Call/Put setups across custom watchlists (`SPY`, `QQQ`, `NVDA`, `TSLA`, etc.).
  - Classifies setups into **Strict**, **Balanced**, and **Aggressive** risk tiers based on trend bias, delta suitability ($\approx 0.40 - 0.45$), spread liquidity, and earnings proximity.
- **Paper Trading Execution**:
  - Live unrealized & realized P&L calculations.
  - Preset and editable **Stop Loss** and **Profit Target** thresholds.
  - Tracks open contracts and logs closed historical trades without wiping session records until manually cleared.
- **Precise Fee Modeling**:
  - Models Moomoo US options execution costs at **$0.69 / contract / side** ($0.65 base commission + $0.025 OCC clearing + $0.0122 ORF pass-through fees).
- **Direct Chart Deep-Linking**:
  - Direct strike resolution to official Moomoo option charts (e.g., `https://www.moomoo.com/options/IWM261007P280000-US`).
- **Hybrid Data Feed**:
  - Seamlessly bridges Yahoo Finance option chains (delayed ~15m) with Moomoo OpenD WebSocket feeds for real-time order book execution.

---

## File Structure

```text
├── index.html       # Single-page terminal frontend
├── server.js        # Lightweight Node.js local proxy bridge
└── README.md        # Documentation and setup instructions