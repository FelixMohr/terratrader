const CryptoJS = require('crypto-js')
const keySize = 256
const iterations = 100
const decrypt = (transitmessage, pass) => {
  try {
    const salt = CryptoJS.enc.Hex.parse(transitmessage.substr(0, 32))
    const iv = CryptoJS.enc.Hex.parse(transitmessage.substr(32, 32))
    const encrypted = transitmessage.substring(64)

    const key = CryptoJS.PBKDF2(pass, salt, {
      keySize: keySize / 32,
      iterations: iterations,
    })

    const decrypted = CryptoJS.AES.decrypt(encrypted, key, {
      iv: iv,
      padding: CryptoJS.pad.Pkcs7,
      mode: CryptoJS.mode.CBC,
    }).toString(CryptoJS.enc.Utf8)
    return decrypted
  } catch (error) {
  console.log(error)
    return ''
  }
}

console.log(decrypt(process.argv[0], process.argv[1]))
