# ChinaASN and IP
- 每日自动更新

</b></详情>
<詳情>
<summary> 数据来源 </summary><br><b>

### ASN： [bgp.he.net](https://bgp.he.net/country/CN)

### IP： [cbuijs/ipasn](https://github.com/cbuijs/ipasn) 
</b></详情>




## 数据源
### ASN： [bgp.he.net](https://bgp.he.net/country/CN)

### IP： [cbuijs/ipasn](https://github.com/cbuijs/ipasn)  


## 应用中使用
### Surge
```
[Rule]
# ChinaASN
RULE-SET, https://raw.githubusercontent.com/iuu666/ASN.China/main/ASN.China.list, Direct
```

### Quantumult X
```
[filter_remote]
# ChinaASN
https://raw.githubusercontent.com/iuu666/ASN.China/main/IP.China.list, tag=ChinaASN, force-policy=direct, update-interval=86400, opt-parser=true, enabled=true
```
