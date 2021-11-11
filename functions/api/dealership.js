const Cloudant = require('@cloudant/cloudant');
const COUCH_URL = "";
const IAM_API_KEY = "";

function http_error( statusCode, message )
{
    let error = new Error( message );
    error.code = statusCode.toString();
    error.statusCode = statusCode;
    return error;
}

async function main( params )
{
    const cloudant = Cloudant( {
        url: COUCH_URL,
        plugins: { iamauth: { iamApiKey: IAM_API_KEY } }
    });
    
    let errorCode = 500;
    let errorMsg = "Something went wrong.";
    
    try
    {
        let mydb = await cloudant.db.use("dealerships");
        let fields = [
            "id",
            "address",
            "city",
            "full_name",
            "lat",
            "long",
            "short_name",
            "st",
            "state",
            "zip"
            ];
        let docList = null;
        if( params.state )
        {
            errorMsg = "The state(" + params.state + ") does not exist."
            let state = params.state.toUpperCase();
            docList = await mydb.find({
                selector : {
                    st : state
                },
                fields : fields
            });
        }
        else if( params.dealer_id )
        {
            errorMsg = "The dealer(" + params.dealer_id + ") does not exist."
            dealer_id = parseInt( params.dealer_id )
            if( !isNaN( dealer_id ) )
            {
                docList = await mydb.find({
                    selector : {
                        id : dealer_id
                    },
                    fields : fields
                });
            }
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
        errorCode = 404;
    }
    catch( error )
    {
        errorCode = 500;
        errorMsg = "Something went wrong.";
    }

    throw http_error( errorCode, errorMsg );
}