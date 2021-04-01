require 'csv'
require 'i18n'



movies_csv = CSV.foreach('output_imdb.csv', headers: true)


actors_ratings = {}

movies_csv.select{|m| m["imdbRating"].to_f > 0 && m["cast"]}.each do |movie|

    movie["cast"].split(",").map{|e| e.strip}.each do |actor|

        if actors_ratings[actor]
            actors_ratings[actor]["total_rating"] += movie["imdbRating"].to_f
            actors_ratings[actor]["count"] += 1
        else
            actors_ratings[actor] = {}
            actors_ratings[actor]["total_rating"] = movie["imdbRating"].to_f
            actors_ratings[actor]["count"] = 1
        end
    end
end




CSV.open("imdb_mean.csv", "w") do |output_csv|

    output_csv << ["actor","imdb_mean"]

    actors_ratings.sort_by{|k,v| k}.map{|k,v| [k,v["total_rating"].to_f/v["count"].to_i]}.map{|e| output_csv << e}


end