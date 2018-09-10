#!/bin/bash


s3cmd put --acl-public --guess-mime-type -r /var/www/html/image.jpg s3://uploads_89/debit_receipt/image.jpg
