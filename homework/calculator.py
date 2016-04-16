"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
def create_list(args):
    """
    Takes a list of String numbers, converts them to int, and breaks out the first number so that we can have that as
     a base to start with when adding, subtracting, etc.  We need this to make iteration easier in the action functions
    :param args: List of numbers that an operand will operate on
    :type args: String

    :return: The First number as a based to be operated on (total) and then a list of all proceeding numbers (numbers)
    """
    args = map(int, args)
    numbers = []
    [numbers.append(arg) for arg in args]
    total = numbers.pop(0)
    return numbers, total


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    numbers, total = create_list(args)
    for num in numbers:
        total += num

    return str(total)


def subtract(*args):
    """ Returns a STRING with subtracting the arguments """
    numbers, total = create_list(args)

    for num in numbers:
        total -= num

    return str(total)


def multiply(*args):
    """ Returns a STRING with multiplying the arguments """
    numbers, total = create_list(args)

    for num in numbers:
        total *= num

    return str(total)


def divide(*args):
    """ Returns a STRING with dividing the arguments """
    numbers, total = create_list(args)
    for num in numbers:
        total /= num

    return str(total)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    args = path.strip("/").split("/")

    func_name = args.pop(0)

    func = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }.get(func_name)

    return func, args


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1> ARE YOU NUTS!?! YOU CAN'T DIVIDE BY ZERO!</h1>"
    except Exception as e:
        status = "500 Internal Server Error"
        body = """<html>
    <head><h1>Calculator</h1></head>
    <h2> You screwed up: {}</h2>
    <p> To use this page, use the URL to do the math.</p>
    <p> The first item in the path represents the operation that is possible. </p>
    <ul>
        <li> /add </li>
        <li> /subtract </li>
        <li> /multiply </li>
        <li> /divide </li>
    </ul>
    <p> Then any proceeding numbers on the path will have that operation acted upon them </p>
    <p></p>
    <h2> Example: </h2>
    <ul>
        <li>http://localhost:8080/multiply/3/5   => 15</li>
        <li>http://localhost:8080/add/23/42      => 65</li>
        <li>http://localhost:8080/subtract/23/42 => -19</li>
        <li>http://localhost:8080/divide/22/11   => 2</li>
    </ul>
    <p>If you have any further questions, you should find a new line of work</p>
    </html>
    """.format(e)
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
