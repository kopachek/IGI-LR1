FROM ruby:3.2

RUN apt-get update -qq && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Gemfile ./
RUN bundle install

COPY . .

CMD until bundle exec rake db:init; do echo "Ожидание базы данных..."; sleep 2; done && \
    bundle exec passenger start -p 3000 --environment development