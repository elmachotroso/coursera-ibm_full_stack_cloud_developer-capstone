const Cloudant = require('@cloudant/cloudant');
const COUCH_URL = "https://0886bfd5-cf1b-4e75-b0bb-e21190990f4f-bluemix.cloudantnosqldb.appdomain.cloud";
const IAM_API_KEY = "P4ML4YSIiBDR3uJoMw_7ymwT_XUSFI5Ikyd_W4fKr52-";

async function main( params )
{
    const cloudant = Cloudant( {
        url: COUCH_URL,
        plugins: { iamauth: { iamApiKey: IAM_API_KEY } }
    });
    
    try
    {
        let mydb = await cloudant.db.use("dealerships");
        let docList = await mydb.list();
        let ids = [];
        docList.rows.forEach( (doc) => {
            ids.push( doc['id'] );
        })
        
        return { "docs" : rows };
    }
    catch( error )
    {
        return { error: error.description };
    }
}