#!/bin/sh
set -e

alembic upgrade head

# If no external Telegram proxy is configured, prepare a local Tor SOCKS5
# fallback. The bot still tries direct IPv4 first and switches to Tor only
# after a network timeout.
if [ -z "${TELEGRAM_PROXY:-}" ]; then
    echo "Preparing local Tor fallback for Telegram..."
    rm -rf /tmp/tor-data
    mkdir -p /tmp/tor-data
    chmod 700 /tmp/tor-data

    tor \
        --SocksPort 9050 \
        --DataDirectory /tmp/tor-data \
        --Log "notice stdout" \
        > /tmp/tor.log 2>&1 &
    TOR_PID=$!

    TOR_READY=0
    i=0
    while [ "$i" -lt 60 ]; do
        if grep -q "Bootstrapped 100%" /tmp/tor.log 2>/dev/null; then
            TOR_READY=1
            break
        fi

        if ! kill -0 "$TOR_PID" 2>/dev/null; then
            echo "Tor fallback exited during startup; continuing with direct IPv4."
            break
        fi

        i=$((i + 1))
        sleep 1
    done

    if [ "$TOR_READY" -eq 1 ]; then
        export TELEGRAM_FALLBACK_PROXY="${TELEGRAM_FALLBACK_PROXY:-socks5://127.0.0.1:9050}"
        echo "Tor fallback is ready."
    else
        echo "Tor fallback was not ready in time; continuing with direct IPv4 only."
        unset TELEGRAM_FALLBACK_PROXY
    fi
fi

exec python bot_runner.py
