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
        let docList = null;
        let errorMsg = "";
        if( state != undefined && state != null )
        {
            errorMsg = "The state does not exist."
            state = state.toUpperCase();
            docList = await mydb.find({
                selector : {
                    st : state
                },
                fields : fields
            })
        }
        else
        {
            errorMsg = "The database is empty."
            docList = await mydb.find({
                selector : {},
                fields : fields
            });
        }
        
        if( docList.docs.length > 0 )
        {
            return { body : docList.docs };
        }
        else
        {
            return {
                code : 404,
                error : errorMsg
            };
        }
    }
    catch( error )
    {
        return {
            code : 500,
            error : error.description
        };
    }
}