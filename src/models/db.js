import { userMongoStore } from "./mongo/user-mongo-store.js";
import { ec2MongoStore } from "./mongo/ec2-mongo-store.js";
import { infoMongoStore } from "./mongo/info-mongo-store.js";
import { adminMongoStore } from "./mongo/admin-mongo-store.js";
import { connectMongo } from "./mongo/connect.js";

export const db = {
  userStore: null,
  ec2Store: null,
  infoStore: null,

  init() {
        this.userStore = userMongoStore;
        this.ec2Store = ec2MongoStore;
        this.infoStore = infoMongoStore;
        this.adminStore = adminMongoStore;
        connectMongo();
    }
};
