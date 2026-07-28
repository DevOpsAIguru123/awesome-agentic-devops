FROM nginx@sha256:4a73073bd557c65b759505da037898b61f1be6cbcc3c2c3aeac22d2a470c1752

COPY nginx.conf /etc/nginx/nginx.conf
COPY --chown=root:root --chmod=0444 index.html styles.css app.js /usr/share/nginx/html/

RUN rm -f /etc/nginx/conf.d/default.conf \
    && mkdir -p /tmp/client_temp /tmp/proxy_temp /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp \
    && chown -R nginx:nginx /tmp/client_temp /tmp/proxy_temp /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp

USER nginx
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD printf 'GET /healthz HTTP/1.0\r\nHost: localhost\r\n\r\n' \
    | nc -w 2 127.0.0.1 8080 \
    | grep -q '200 OK'

CMD ["nginx", "-g", "daemon off;"]
