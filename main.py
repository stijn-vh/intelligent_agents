from query_handler import QueryHandler

if __name__ == "__main__":
    query_handler = QueryHandler()

    r = query_handler.get_persons_with_place_and_occupation('Kitchen', 'Guest')
    query_handler.print_results(r)