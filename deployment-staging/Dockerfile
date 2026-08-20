FROM prefecthq/prefect:3-latest

COPY deployment-staging/configuration.py /opt/staging/configuration.py
COPY deployment-staging/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENV PREFECT_HOME=/opt/prefect
EXPOSE 4200

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
