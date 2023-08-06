# AWS Credentials

This tool lets you easily manage AWS IAM Credentials for a user.

## Usage
```
⇒  aws-credentials --help
Usage: aws-credentials [OPTIONS] COMMAND [ARGS]...

  CLI utility for managing access keys.

Options:
  -v, --verbose  Increase the verbosity of messages: "-v" for normal output,
                 and "-vv" for more verbose output.
  -h, --help     Show this message and exit.

Commands:
  activate    Activate a specific access key.
  create      Create a new access key.
  deactivate  Deactivate a specific access key.
  delete      Delete a specific access key.
  list        List access keys.
  rotate      Rotate AWS credentials.
```

**activate**
```
⇒  aws-credentials activate --help
Usage: aws-credentials activate [OPTIONS] ACCESS_KEY_ID

  Activate a specific access key.

  ACCESS_KEY_ID is the id of the key to activate.

Options:
  --access-key TEXT     AWS_ACCESS_KEY_ID to use.
  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.
  --session-token TEXT  AWS_SESSION_TOKEN to use.
  -h, --help            Show this message and exit.
```

**create**
```
⇒  aws-credentials create --help
Usage: aws-credentials create [OPTIONS]

  Create a new access key.

Options:
  --access-key TEXT     AWS_ACCESS_KEY_ID to use.
  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.
  --session-token TEXT  AWS_SESSION_TOKEN to use.
  -h, --help            Show this message and exit.
```

**deactivate**
```
⇒  aws-credentials deactivate --help
Usage: aws-credentials deactivate [OPTIONS] ACCESS_KEY_ID

  Deactivate a specific access key.

  ACCESS_KEY_ID is the id of the key to deactivate.

Options:
  --access-key TEXT     AWS_ACCESS_KEY_ID to use.
  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.
  --session-token TEXT  AWS_SESSION_TOKEN to use.
  -h, --help            Show this message and exit.
```

**delete**
```
⇒  aws-credentials delete --help
Usage: aws-credentials delete [OPTIONS] ACCESS_KEY_ID

  Delete a specific access key.

  ACCESS_KEY_ID is the id of the key to delete.

Options:
  --access-key TEXT     AWS_ACCESS_KEY_ID to use.
  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.
  --session-token TEXT  AWS_SESSION_TOKEN to use.
  -h, --help            Show this message and exit.
```

**list**
```
⇒  aws-credentials list --help
Usage: aws-credentials list [OPTIONS]

  List access keys.

Options:
  --access-key TEXT     AWS_ACCESS_KEY_ID to use.
  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.
  --session-token TEXT  AWS_SESSION_TOKEN to use.
  -h, --help            Show this message and exit.
```

**rotate**
```
⇒  aws-credentials rotate --help
Usage: aws-credentials rotate [OPTIONS]

  Rotate AWS credentials.

  This will delete inactive keys before creating the new key. It will then
  deactivate the old key.

Options:
  --access-key TEXT     AWS_ACCESS_KEY_ID to use.
  --secret-key TEXT     AWS_SECRET_ACCESS_KEY to use.
  --session-token TEXT  AWS_SESSION_TOKEN to use.
  -h, --help            Show this message and exit.
```
