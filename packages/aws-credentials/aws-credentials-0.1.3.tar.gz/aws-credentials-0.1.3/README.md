# AWS Credentials

This tool lets you easily manage AWS IAM Credentials for a user.

## Usage
```
⇒  aws-credentials --help
Usage: aws-credentials [OPTIONS] COMMAND [ARGS]...

  CLI utility for managing access keys.

Options:
  --access_key TEXT  AWS_ACCESS_KEY_ID to use
  --secret_key TEXT  AWS_SECRET_ACCESS_KEY to use
  -v, --verbose
  --help             Show this message and exit.

Commands:
  activate
  create
  deactivate
  delete
  list
  rotate
```

**activate**
```
⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials activate --help
Usage: aws-credentials activate [OPTIONS] ACCESS_KEY

Options:
  --help  Show this message and exit.
```

**create**
```
⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials create --help
Usage: aws-credentials create [OPTIONS]

Options:
  --help  Show this message and exit.
```

**deactivate**
```
⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials deactivate --help
Usage: aws-credentials deactivate [OPTIONS] ACCESS_KEY

Options:
  --help  Show this message and exit.
```

**delete**
```
⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials delete --help
Usage: aws-credentials delete [OPTIONS] ACCESS_KEY

Options:
  --help  Show this message and exit.
```

**list**
```
⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials list --help
Usage: aws-credentials list [OPTIONS]

Options:
  --help  Show this message and exit.
```

**rotate**
```
⇒  AWS_ACCESS_KEY_ID=key AWS_SECRET_ACCESS_KEY=secret aws-credentials rotate --help
Usage: aws-credentials rotate [OPTIONS]

Options:
  --help  Show this message and exit.
```
