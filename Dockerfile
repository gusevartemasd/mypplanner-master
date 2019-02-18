FROM registry.gitlab.com/mypplanner/docker-django

ENV PYTHONUNBUFFERED 1

ARG src=/usr/src/app

WORKDIR $src

ADD . .

RUN apk add --no-cache nginx

RUN ./manage.py collectstatic --no-input
RUN ./manage.py compilemessages

EXPOSE 80

ADD entrypoint.sh /usr/local/bin/
ADD nginx.default.conf /etc/nginx/conf.d/default.conf

CMD ["/usr/local/bin/entrypoint.sh"]
