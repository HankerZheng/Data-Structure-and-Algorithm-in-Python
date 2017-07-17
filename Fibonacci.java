public class Fibonacci {
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

    public static void main(String[] args) {
        Fibonacci f = new Fibonacci();
        for (int i = 0; i < 500; i ++) {
            int ans = f.solution(i);
            System.out.println(ans);
        }
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