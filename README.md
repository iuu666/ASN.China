# ChinaASN or ChinaIP
ChinaASN和IP数据库的实时更新


## Features
- 每日自动更新
- 可靠且准确的来源


## Data Source
### ASN Information
- [bgp.he.net](https://bgp.he.net/country/CN)

### IP Information
- [cbuijs/ipasn](https://github.com/cbuijs/ipasn)


## Use in proxy app
### Surge
```
[Rule]
# > China ASN List
RULE-SET, https://raw.githubusercontent.com/missuo/ASN-China/main/ASN.China.list, Direct
```

### Quantumult X
```
[filter_remote]
# China ASN List
https://raw.githubusercontent.com/missuo/ASN-China/main/ASN.China.list, tag=ChinaASN, force-policy=direct, update-interval=86400, opt-parser=true, enabled=true
```



## Author

**ASN-China** © [Vincent Young](https://github.com/missuo), Released under the [MIT](./LICENSE) License.<br>


