# exprstack
Stack-based math expression evaluator.

## Examples
```sh
$ python3 exprstack.py "2 3 + ."
5
$ python3 exprstack.py "9 3 * dup ^ ."
443426488243037769948249630619149892803
$ python3 exprstack.py "0 0 / ."
error: cannot divide by 0
$ python3 exprstack.py "0 0 ^ ."
error: 0^0 is undefined
```
