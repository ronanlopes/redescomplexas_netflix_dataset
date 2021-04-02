require 'uri'
require 'csv'
require 'json'
require 'net/http'

movies_csv = CSV.foreach('netflix_titles.csv')
movies_csv = movies_csv.to_a

current_number = CSV.foreach('output_imdb.csv').to_a.size.to_i
number_to_crawl = 950


CSV.open("output_imdb.csv", "a") do |output_csv|

    movies_csv[current_number..(current_number+number_to_crawl)].each do |m|
        puts m[2]
        uri = URI.parse('http://www.omdbapi.com')
        params = { :t => m[2], :apikey => "a3eb2bb8" }
        uri.query = URI.encode_www_form( params )
        res = JSON.parse(Net::HTTP.get(uri))
        output_csv << (m + [res["imdbRating"].to_f])
    end


end