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
        let dbParams = { include_docs : true };
        let fields = [
            "_id",
            "_rev",
            "address",
            "city",
            "full_name",
            "id",
            "lat",
            "long",
            "short_name",
            "st",
            "state",
            "zip"
            ];
        let state = params.state;
        if( state != undefined && state != null )
        {
            state = state.toUpperCase();
            let docList = await mydb.find({
                "selector" : {
                    "st" : state
                },
                "fields" : fields
            })
            return { "body" : docList.docs };
        }
        
        let docList = await mydb.find({
            "selector" : {
            },
            "fields" : fields
        })
        return { "body" : docList.docs };
    }
    catch( error )
    {
        return { error: error.description };
    }
}