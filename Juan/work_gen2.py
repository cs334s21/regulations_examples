from utility_functions import write_all_itemsIDs_in_parentItem_to_file
from utility_functions import comment_url
from utility_functions import get_key
from query_options import add_key_to_params

params = {}
add_key_to_params(get_key(), params)
write_all_itemsIDs_in_parentItem_to_file("comments", comment_url(), params)