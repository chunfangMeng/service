
def paginate(data, page, per_page):
    total = len(data)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    if end > total:
        end = total
    return data[start:end], total_pages
