require 'sinatra'
require 'sinatra/activerecord'

set :database_file, 'config/database.yml'

class Visit < ActiveRecord::Base
end

get '/' do
  Visit.create
  @count = Visit.count
  "<h1>Ruby App (Passenger + ActiveRecord)</h1>
   <p>Статус: <b>Работает</b></p>
   <p>Всего визитов в базе: <b>#{@count}</b></p>"
end