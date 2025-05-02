FROM minio/mc

COPY init-minio.sh /init-minio.sh
RUN chmod +x /init-minio.sh

ENTRYPOINT ["/init-minio.sh"]
