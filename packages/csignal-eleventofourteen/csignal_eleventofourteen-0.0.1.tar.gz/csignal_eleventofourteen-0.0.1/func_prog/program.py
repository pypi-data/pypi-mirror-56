def isLucky(n):
    r=str(n)
    t=0
    s=0
    for i in range(int(len(r)/2)):
        t=t+int(r[i])
    for j in range(int(len(r)/2),len(r)):
        s=s+int(r[j])
    if t==s:
        return True
    else:
        return False


def sortByHeight(a):
    s=[]
    d=[]
    b=[]
    c=-1
    for i in range(len(a)):
        if a[i]==-1:
            s.append(i)
        else:
            d.append(a[i])
    l=sorted(d)
    for j in range(len(a)):
        if j in s:
            b.append(-1)
        else:
            c=c+1
            b.append(l[c])
    return b

def reverseInParentheses(s):
    for i in range(len(s)):
        if s[i]=="(":
            start=i
        if s[i]==")":
            end=i
            return reverseInParentheses(s[:start]+s[start+1:end][::-1]+s[end+1:])
    return s


def alternatingSums(a):
    team1=[]
    team2=[]
    for i in range(len(a)):
        if i%2==0:
            team1.append(a[i])
        else:
            team2.append(a[i])
    return(sum(team1),sum(team2))