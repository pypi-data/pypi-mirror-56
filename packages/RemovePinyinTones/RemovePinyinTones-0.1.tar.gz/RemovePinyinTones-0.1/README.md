# Remove pinyin tones from pinyin
## logics
### pinyin tone mapping  
  
    | from | to |  
    | - | - |  
    | ā | a |  
    | á | a |  
    | ǎ | a |  
    | à | a |  
    | ō | o |  
    | ó | o |  
    | ǒ | o |  
    | ò | o |  
    | ē | e |  
    | é | e |  
    | ě | e |  
    | è | e |  
    | ī | i |  
    | í | i |  
    | ǐ | i |  
    | ì | i |  
    | ū | u |  
    | ú | u |  
    | ǔ | u |  
    | ù | u |  
    | ǖ | v |  
    | ǘ | v |  
    | ǚ | v |  
    | ǜ | v |  
    | ü | v |  
    | ń | n |  
    | ň | n |  
    | ǹ | n |  
    | ẑ | z |  
    | ĉ | c |  
    | ŝ | s |  
    | ɡ | g |  
    | ɑ | a |  

### examples  
    from RemovePinyinTones import RemovePinyinTones
    RemovePinyinTones.remove('xiǎo')
