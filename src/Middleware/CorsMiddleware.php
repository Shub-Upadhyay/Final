<?php

declare(strict_types=1);

namespace App\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\RequestHandlerInterface;
use Psr\Http\Server\MiddlewareInterface;

class CorsMiddleware implements MiddlewareInterface
{
	public function process(
		ServerRequestInterface $request,
		RequestHandlerInterface $handler
	): ResponseInterface {
		// Calling $handler->handle() delegates control to the *next* middleware
		// In your application's queue.
		$response = $handler->handle($request);

		// $response = $response
		// 	->withHeader('Access-Control-Allow-Origin', '*')
		// 	->withHeader('Access-Control-Allow-Methods', '*');

		return $response;
	}
}
