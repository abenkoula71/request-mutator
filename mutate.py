#! /usr/bin/python3

import sys
import importlib

class HttpMutator:
    def __init__(self, module, request):
        self.mod = importlib.import_module("modules." + module)
        if self.mod.mutate == None:
            raise Exception("Invalid module name")
        with open(request, 'r') as reqfile:
            self.data = reqfile.readlines()
    def mutate(self):
      try:
        cookies = dict()
        headers = dict()
        method = self.data[0]
        method = method[:method.index(' ')]
        if not method in ["POST", "GET", "PUT", "DELETE", "PATCH"]:
            raise Exception("Invalid request type")
        url = self.data[0][len(method) + 1:]
        url = url[:url.index(' ')]
        for line in self.data[1:]:
            what = line[:line.index(':')]
            if (what == 'Host' and not url.startswith("http")):
                url = "https://" + line[line.index(':')+2:].strip() + url
            elif (what == 'Cookie'):
                cook = line[line.index(':')+1:].strip()
                all_cookies = cook.split(";")
                for c in all_cookies:
                    if c.startswith(" "):
                        c = c[1:]
                    a = c[:c.index("=")]
                    b = c[c.index("=")+1:]
                    cookies[a] = b
            else:
                headers[what] = line[line.index(':')+1:].strip()
        return self.mod.mutate(method, url, headers, cookies)
      except Exception as e:
         raise Exception("Error decoding requests file!" + str(e))
         

if __name__ == "__main__":
    try:
        mutator = HttpMutator(sys.argv[1], sys.argv[2])
        print(mutator.mutate())
    except IndexError:
        print("Invalid parameters \n\n\t-> usage ./mutate.py how request.file\n\n")
    except Exception as e:
        print(str(e))

