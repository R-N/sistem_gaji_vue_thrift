//
// Autogenerated by Thrift Compiler (0.13.0)
//
// DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
//
"use strict";

var thrift = require('thrift');
var Thrift = thrift.Thrift;
var Q = thrift.Q;
var Int64 = require('node-int64');


var ttypes = module.exports = {};
ttypes.UserRole = {
  'ADMIN_BIASA' : 0,
  'ADMIN_UTAMA' : 1,
  'ADMIN_AKUN' : 2,
  'PENGAWAS' : 3,
  'SUPER_ADMIN' : 4
};
ttypes.LoginErrorCode = {
  'USERNAME_KOSONG' : 0,
  'PASSWORD_KOSONG' : 1,
  'USERNAME_PASSWORD_SALAH' : 2,
  'REFRESH_TOKEN_INVALID' : 3,
  'REFRESH_TOKEN_EXPIRED' : 4,
  'ALREADY_LOGGED_IN' : 5
};
ttypes.AuthErrorCode = {
  'NOT_LOGGED_IN' : 0,
  'AUTH_TOKEN_INVALID' : 1,
  'AUTH_TOKEN_EXPIRED' : 2,
  'INVALID_ROLE' : 3,
  'NO_PERMISSION' : 4
};
var User = module.exports.User = function(args) {
  this.name = null;
  this.role = null;
  if (args) {
    if (args.name !== undefined && args.name !== null) {
      this.name = args.name;
    }
    if (args.role !== undefined && args.role !== null) {
      this.role = args.role;
    }
  }
};
User.prototype = {};
User.prototype.read = function(input) {
  input.readStructBegin();
  while (true) {
    var ret = input.readFieldBegin();
    var ftype = ret.ftype;
    var fid = ret.fid;
    if (ftype == Thrift.Type.STOP) {
      break;
    }
    switch (fid) {
      case 1:
      if (ftype == Thrift.Type.STRING) {
        this.name = input.readString();
      } else {
        input.skip(ftype);
      }
      break;
      case 2:
      if (ftype == Thrift.Type.I32) {
        this.role = input.readI32();
      } else {
        input.skip(ftype);
      }
      break;
      default:
        input.skip(ftype);
    }
    input.readFieldEnd();
  }
  input.readStructEnd();
  return;
};

User.prototype.write = function(output) {
  output.writeStructBegin('User');
  if (this.name !== null && this.name !== undefined) {
    output.writeFieldBegin('name', Thrift.Type.STRING, 1);
    output.writeString(this.name);
    output.writeFieldEnd();
  }
  if (this.role !== null && this.role !== undefined) {
    output.writeFieldBegin('role', Thrift.Type.I32, 2);
    output.writeI32(this.role);
    output.writeFieldEnd();
  }
  output.writeFieldStop();
  output.writeStructEnd();
  return;
};

var LoginResult = module.exports.LoginResult = function(args) {
  this.auth_token = null;
  this.refresh_token = null;
  if (args) {
    if (args.auth_token !== undefined && args.auth_token !== null) {
      this.auth_token = args.auth_token;
    } else {
      throw new Thrift.TProtocolException(Thrift.TProtocolExceptionType.UNKNOWN, 'Required field auth_token is unset!');
    }
    if (args.refresh_token !== undefined && args.refresh_token !== null) {
      this.refresh_token = args.refresh_token;
    }
  }
};
LoginResult.prototype = {};
LoginResult.prototype.read = function(input) {
  input.readStructBegin();
  while (true) {
    var ret = input.readFieldBegin();
    var ftype = ret.ftype;
    var fid = ret.fid;
    if (ftype == Thrift.Type.STOP) {
      break;
    }
    switch (fid) {
      case 1:
      if (ftype == Thrift.Type.STRING) {
        this.auth_token = input.readString();
      } else {
        input.skip(ftype);
      }
      break;
      case 2:
      if (ftype == Thrift.Type.STRING) {
        this.refresh_token = input.readString();
      } else {
        input.skip(ftype);
      }
      break;
      default:
        input.skip(ftype);
    }
    input.readFieldEnd();
  }
  input.readStructEnd();
  return;
};

LoginResult.prototype.write = function(output) {
  output.writeStructBegin('LoginResult');
  if (this.auth_token !== null && this.auth_token !== undefined) {
    output.writeFieldBegin('auth_token', Thrift.Type.STRING, 1);
    output.writeString(this.auth_token);
    output.writeFieldEnd();
  }
  if (this.refresh_token !== null && this.refresh_token !== undefined) {
    output.writeFieldBegin('refresh_token', Thrift.Type.STRING, 2);
    output.writeString(this.refresh_token);
    output.writeFieldEnd();
  }
  output.writeFieldStop();
  output.writeStructEnd();
  return;
};

var LoginError = module.exports.LoginError = function(args) {
  Thrift.TException.call(this, "LoginError");
  this.name = "LoginError";
  this.code = null;
  if (args) {
    if (args.code !== undefined && args.code !== null) {
      this.code = args.code;
    }
  }
};
Thrift.inherits(LoginError, Thrift.TException);
LoginError.prototype.name = 'LoginError';
LoginError.prototype.read = function(input) {
  input.readStructBegin();
  while (true) {
    var ret = input.readFieldBegin();
    var ftype = ret.ftype;
    var fid = ret.fid;
    if (ftype == Thrift.Type.STOP) {
      break;
    }
    switch (fid) {
      case 1:
      if (ftype == Thrift.Type.I32) {
        this.code = input.readI32();
      } else {
        input.skip(ftype);
      }
      break;
      case 0:
        input.skip(ftype);
        break;
      default:
        input.skip(ftype);
    }
    input.readFieldEnd();
  }
  input.readStructEnd();
  return;
};

LoginError.prototype.write = function(output) {
  output.writeStructBegin('LoginError');
  if (this.code !== null && this.code !== undefined) {
    output.writeFieldBegin('code', Thrift.Type.I32, 1);
    output.writeI32(this.code);
    output.writeFieldEnd();
  }
  output.writeFieldStop();
  output.writeStructEnd();
  return;
};

var AuthError = module.exports.AuthError = function(args) {
  Thrift.TException.call(this, "AuthError");
  this.name = "AuthError";
  this.code = null;
  if (args) {
    if (args.code !== undefined && args.code !== null) {
      this.code = args.code;
    }
  }
};
Thrift.inherits(AuthError, Thrift.TException);
AuthError.prototype.name = 'AuthError';
AuthError.prototype.read = function(input) {
  input.readStructBegin();
  while (true) {
    var ret = input.readFieldBegin();
    var ftype = ret.ftype;
    var fid = ret.fid;
    if (ftype == Thrift.Type.STOP) {
      break;
    }
    switch (fid) {
      case 1:
      if (ftype == Thrift.Type.I32) {
        this.code = input.readI32();
      } else {
        input.skip(ftype);
      }
      break;
      case 0:
        input.skip(ftype);
        break;
      default:
        input.skip(ftype);
    }
    input.readFieldEnd();
  }
  input.readStructEnd();
  return;
};

AuthError.prototype.write = function(output) {
  output.writeStructBegin('AuthError');
  if (this.code !== null && this.code !== undefined) {
    output.writeFieldBegin('code', Thrift.Type.I32, 1);
    output.writeI32(this.code);
    output.writeFieldEnd();
  }
  output.writeFieldStop();
  output.writeStructEnd();
  return;
};

