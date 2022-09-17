def average_rating(rating_list):		# helper method to calculate average rating of book
    if not rating_list:
        return 0

    return round(sum(rating_list) / len(rating_list))
