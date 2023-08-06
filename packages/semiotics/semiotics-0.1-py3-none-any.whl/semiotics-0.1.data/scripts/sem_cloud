import urllib3
import urllib

class SemCloud:
    def __init__(self, email, channel_id):
        self.semail = email
        self.schannelid = channel_id

    def write_data(self,field1=0,field2=0,field3=0,field4=0):
        url = "http://mytechnology.in/postdata.php?email="+self.semail+"&channelid="+self.schannelid

        if field1 != 0 and field2 == 0 and field3 == 0 and field4 == 0:
            url += "&field1=" + str(field1)

        elif field1 != 0 and field2 != 0 and field3 == 0 and field4 == 0:
            url += "&field1=" + str(field1) + "&field2=" + str(field2)

        elif field1 != 0 and field2 != 0 and field3 != 0 and field4 == 0:
            url += "&field1=" + str(field1) + "&field2=" + str(field2) + "&field3=" + str(field3)

        elif field1 != 0 and field2 != 0 and field3 != 0 and field4 != 0:
            url += "&field1=" + str(field1) + "&field2=" + str(field2) + "&field3=" + str(field3)
            url += "&field4=" + str(field4)

        http = urllib3.PoolManager()

        response = http.request('GET', url)
        code = response.status
        print("Server status:")
        print(code)
        print("Server Response:")
        print(response.data)

