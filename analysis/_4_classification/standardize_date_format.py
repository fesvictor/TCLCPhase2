""" Current date format from each sources
{
    'blog': '20170728',
    'facebook': '2017-05-18 06:24:38',
    'lowyat': '20170102',
    'twitter': 'Wed Jan 11 06:48:37 +0000 2017',
    'jbtalks': '20160304'
}
 """
def standardize_date_format(all_posts):
    for post in all_posts:
        if post['source'] == 'facebook':
            post['date'] = correct_date_format_of_facebook(post['date'])
        elif post['source'] == 'twitter':
            post['date'] = correct_date_format_of_twitter(post['date'])
    return all_posts

def correct_date_format_of_facebook(date):
    return ''.join(date.split(' ')[0].split('-'))

def correct_date_format_of_twitter(date):
    months = {
        '01': 'Jan', '02': 'Feb', '03': 'Mar',
        '04': 'Apr', '05': 'May', '06': 'Jun',
        '07': 'Jul', '08': 'Aug', '09': 'Sep',
        '10': 'Oct', '11': 'Nov', '12': 'Dec'
    }
    months = {v: k for k, v in months.items()}
    tokens = date.split(' ')
    day = tokens[2]
    month = months[tokens[1]]
    year = tokens[-1]
    return year + month + day.zfill(2)