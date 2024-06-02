twitter_login(driver, email, password)
    top_trends = fetch_trending_topics(driver)
    unique_id = str(uuid.uuid4())
    ip_address = proxy.split('@')[-1].split(':')[0]  # Extract IP from proxy
    end_time = datetime.now()
    
    # Store results in MongoDB
    result = {
        "unique_id": unique_id,
        "trend1": top_trends[0] if len(top_trends) > 0 else "",
        "trend2": top_trends[1] if len(top_trends) > 1 else "",
        "trend3": top_trends[2] if len(top_trends) > 2 else "",
        "trend4": top_trends[3] if len(top_trends) > 3 else "",
        "trend5": top_trends[4] if len(top_trends) > 4 else "",
        "date_time": end_time,
        "ip_address": ip_address
    }
    collection.insert_one(result)