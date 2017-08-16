// For nature number n, we have
//      Fib(2n)   = Fib(n+1)^2 - Fib(n-1)^2
//      Fib(2n+1) = Fib(n)  ^2 + Fib(n+1)^2


public class Fibonacci {

    public static void main(String[] args) {
        Fibonacci f = new Fibonacci();
        int[] res = new int[90];
        for (int i = 0; i < res.length; i++) {
            res[i] = f.solution(i);
        }
        for (int i = 1; i < 50; i += 2) {
            int calculate = res[i/2] * res[i/2] + res[i/2+1] * res[i/2+1];
            if (calculate != res[i]) {
                System.out.format("%d SQX's Ans: %d; Ans: %d\n",i, calculate, res[i]);
            }
        }
    }


    public int solution(int n) {
        TwoTwo ans = new TwoTwo(1,0,0,1);
        TwoTwo tmp = new TwoTwo(1,1,1,0);
        int left = n;
        while (left > 0) {
            if ((left & 1) == 1) ans.times(tmp);
            tmp.power();
            left = left >> 1;
        }
        return (int) ans.c;
    }
}

class TwoTwo {
    long a;
    long b;
    long c;
    long d;

    public TwoTwo(long a, long b, long c, long d) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
    }

    public void times(TwoTwo t1) {
        long ta = (a * t1.a + b * t1.c) % 1000000;
        long tb = (a * t1.b + b * t1.d) % 1000000;
        long tc = (c * t1.a + d * t1.c) % 1000000;
        long td = (c * t1.b + d * t1.d) % 1000000;
        a = ta;
        b = tb;
        c = tc;
        d = td;
    }

    public void power() {
        long ta = (a * a + b * c) % 1000000;
        long tb = (a * b + b * d) % 1000000;
        long tc = (a * c + c * d) % 1000000;
        long td = (b * c + d * d) % 1000000;
        a = ta;
        b = tb;
        c = tc;
        d = td;
    }

    public String toString() { 
        return a + " " + b + " " + c + " " + d;
    }
}