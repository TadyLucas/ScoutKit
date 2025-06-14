use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use trust_dns_resolver::config::*;
use trust_dns_resolver::Resolver;
use rayon::prelude::*;
use url::Url;

fn extract_domain(url: &str) -> Option<String> {
    Url::parse(url).ok()?.host_str().map(|h| h.to_string())
}

fn load_wordlist(path: &str) -> Vec<String>{
    let file = File::open(path).expect("Failed to open wordlist");
    BufReader::new(file).lines().filter_map(Result::ok).collect()
}

fn resolve_subdomain(sub: &str, resolver: &Resolver) -> Option<String> {
    println!("Resolving: {}", sub);
    match resolver.lookup_ip(sub) {
        Ok(_response) => {
            println!("Success: {}", sub);
            Some(sub.to_string())
        },
        Err(err) => {
            println!("Failed: {} ({})", sub, err);
            None
        }
    }
}


fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3{
        std::process::exit(1);
    }

    let url = &args[1];
    let wordlist_path = &args[2];

    println!("Using wordlist: {}", wordlist_path);
    
    
    let Some(domain) = extract_domain(url) else {
        std::process::exit(1);
    };
    
    println!("Target domain: {}", domain);
    let words = load_wordlist(wordlist_path);
    let resolver = Resolver::new(ResolverConfig::default(), ResolverOpts::default()).unwrap();

   let subdomains: Vec<String> = words.par_iter()
        .map(|word| format!("{}.{}", word, domain))
        .filter_map(|sub| resolve_subdomain(&sub, &resolver))
        .collect();

    for sub in subdomains {
        println!("{}", sub);
    }
}
