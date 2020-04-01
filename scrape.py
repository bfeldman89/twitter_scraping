# !/usr/bin/env python
"""This module does blah blah."""
import datetime
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# edit these three variables
start = datetime.datetime(2018, 1, 1)  # year, month, day
end = datetime.datetime(2019, 12, 7)  # year, month, day

# only edit these if you're having problems
delay = 20  # time to wait on each page load before reading the page
driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()


# don't mess with this stuff
twitter_ids_filename = 'all_ids.json'
days = (end - start).days + 1
months = int(days / 30)
id_selector = '.time a.tweet-timestamp'
tweet_selector = 'li.js-stream-item'
ids = []


def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)
                                         ) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])


def form_url(user, since, until):
    root = 'https://twitter.com'
    q1 = f"from%3A{user}%20since%3A{since}%20until%3A{until}&src=typed_query&f=video"
    return f"{root}/search?q={q1}"


def increment_day(date, i):
    return date + datetime.timedelta(days=i)


for instance in range(months):
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 30))
    url = form_url('bfeldman89', d1, d2)
    print(url)
    print(d1)
    driver.get(url)
    sleep(delay)

    try:
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        increment = 10

        while len(found_tweets) >= increment:
            print('scrolling down to load more tweets')
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment += 10

        print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))

        for tweet in found_tweets:
            try:
                tid = tweet.find_element_by_css_selector(
                    id_selector).get_attribute('href').split('/')[-1]
                ids.append(tid)
            except StaleElementReferenceException as e:
                print('lost element reference', tweet)

    except NoSuchElementException:
        print('no tweets on this day')

    start = increment_day(start, 30)


try:
    with open(twitter_ids_filename) as f:
        all_ids = ids + json.load(f)
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))
except FileNotFoundError:
    with open(twitter_ids_filename, 'w') as f:
        all_ids = ids
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))

with open(twitter_ids_filename, 'w') as outfile:
    json.dump(data_to_write, outfile)

print('all done here')
driver.close()
